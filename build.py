#!/usr/bin/env python3
"""Builds public/index.html from src/app.html (the app itself) plus the website head.
Run: python3 build.py   (no dependencies)"""
import pathlib,re
root=pathlib.Path(__file__).parent
app=(root/'src'/'app.html').read_text()
app=re.sub(r'^\s*<title>.*?</title>\s*','',app,count=1)
app=re.sub(r'<meta name="claude:[^>]*>\s*','',app)
head='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0E6B57" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1513" media="(prefers-color-scheme: dark)">
<meta name="description" content="Plan your budget, track spending and paychecks, and estimate Puerto Rico income tax.">
<title>Finance Planning</title>
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Finance">
<style>body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
<script src="/vendor/supabase-2.118.0.js"></script>
<script>
window.FP_SUPABASE={url:'https://pqrkysbqufrxvqvxnibc.supabase.co',
  key:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBxcmt5c2JxdWZyeHZxdnhuaWJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM0MDY1OTgsImV4cCI6MjEwODk4MjU5OH0.GFPDe8uh-PlMSaWSBCYIbzu66qN71_dmRNk8wTlYNos',
  google:false};
if('serviceWorker' in navigator&&location.protocol==='https:'){window.addEventListener('load',()=>{navigator.serviceWorker.register('/sw.js').catch(()=>{});});}
</script>
</head><body>
'''
(root/'public'/'index.html').write_text(head+app+'\n</body></html>\n')
print('index.html written,',len(head+app),'bytes')
