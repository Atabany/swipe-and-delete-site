import puppeteer from '../../Tools/AppPreview/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import fs from 'node:fs';
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{
const page=await browser.newPage();await page.setViewport({width:1200,height:630,deviceScaleFactor:1});
const icon=fs.readFileSync(new URL('../assets/app-icon.webp',import.meta.url)).toString('base64');
await page.setContent(`<html><style>*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#0e0f12;color:#f2f3f5;font-family:Arial,sans-serif;padding:64px 80px}.brand{display:flex;align-items:center;gap:20px;font-size:24px}img{width:70px;height:70px;border-radius:18px}h1{font-size:78px;line-height:1.04;letter-spacing:-4px;margin:65px 0 28px}h1 span{color:#e8b566}p{font-size:24px;color:#b0b2ba}.tag{position:absolute;right:70px;bottom:70px;border:1px solid #303239;border-radius:40px;padding:15px 25px;color:#e8b566}</style><div class="brand"><img src="data:image/webp;base64,${icon}">Photo Cleaner: Swipe &amp; Delete</div><h1>Keep the memories.<br><span>Lose the extras.</span></h1><p>A personal cleanup plan for your iPhone.</p><div class="tag">Your photos. Your decisions.</div></html>`);
await page.screenshot({path:new URL('../assets/og.png',import.meta.url).pathname});
}finally{await browser.close();}
