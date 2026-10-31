-- Finance Planning: database setup.
-- Paste all of this into Supabase → SQL Editor → New query, then click Run.
-- Safe to run more than once.

-- One row per person: everything except expenses (income, plan, goals, settings), as JSON.
create table if not exists public.user_settings (
  user_id    uuid primary key default auth.uid() references auth.users(id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  constraint user_settings_size check (pg_column_size(data) < 2000000)
);

-- One row per expense.
create table if not exists public.expenses (
  user_id    uuid not null default auth.uid() references auth.users(id) on delete cascade,
  id         text not null check (char_length(id) between 1 and 200),
  data       jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (user_id, id),
  constraint expenses_size check (pg_column_size(data) < 20000)
);

-- Row level security: a signed-in person can only see and change their own rows.
alter table public.user_settings enable row level security;
alter table public.expenses      enable row level security;

drop policy if exists "Own settings" on public.user_settings;
create policy "Own settings" on public.user_settings
  for all to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists "Own expenses" on public.expenses;
create policy "Own expenses" on public.expenses
  for all to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

revoke all on public.user_settings, public.expenses from anon;
grant select, insert, update, delete on public.user_settings, public.expenses to authenticated;

-- "Delete account" in Settings: removes the signed-in person and, through the
-- cascades above, all of their data.
create or replace function public.delete_my_account()
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if auth.uid() is null then
    raise exception 'Not signed in';
  end if;
  delete from auth.users where id = auth.uid();
end;
$$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
