'use strict';
const video=document.querySelector('video[data-motion]');
const motionButton=document.getElementById('motion-toggle');
if(video&&motionButton){
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let userPaused=false;
 const restricted=()=>reduced.matches||Boolean(navigator.connection?.saveData);
 const sync=()=>{
  if(restricted()||userPaused||document.hidden){video.pause();motionButton.textContent='Play animation';}
  else{if(!video.src) video.src=video.dataset.src;video.play().then(()=>{motionButton.textContent='Pause animation';}).catch(()=>{motionButton.textContent='Play animation';});}
 };
 motionButton.hidden=false;
 motionButton.addEventListener('click',()=>{if(video.paused){userPaused=false;if(!video.src)video.src=video.dataset.src;video.play().then(()=>motionButton.textContent='Pause animation').catch(()=>{});}else{userPaused=true;sync();}});
 reduced.addEventListener('change',sync);document.addEventListener('visibilitychange',sync);sync();
}
const form=document.getElementById('cleanup-planner');
if(form){
 const result=document.getElementById('planner-result');
 const read=id=>Number(document.getElementById(id).value);
 const update=()=>{
  if(!form.checkValidity()){result.innerHTML='<p>Enter valid non-negative counts and sizes. Average sizes must be greater than zero.</p>';return;}
  const photos=read('photos'),photoSize=read('photo-size'),screens=read('screenshots'),screenSize=read('screen-size'),videos=read('videos'),videoSize=read('video-size');
  const rows=[{name:'unwanted photos',count:photos,mb:photos*photoSize},{name:'old screenshots',count:screens,mb:screens*screenSize},{name:'unwanted videos',count:videos,mb:videos*videoSize}];
  const total=rows.reduce((sum,row)=>sum+row.mb,0);const max=rows.reduce((a,b)=>b.mb>a.mb?b:a,rows[0]);
  result.replaceChildren();
  const strong=document.createElement('strong');strong.textContent=(total/1000).toLocaleString(undefined,{maximumFractionDigits:2})+' GB estimated';result.append(strong);
  const text=document.createElement('p');text.textContent=total>0?'Start with '+max.name+': '+max.count.toLocaleString()+' items account for about '+(max.mb/1000).toLocaleString(undefined,{maximumFractionDigits:2})+' GB of this estimate.':'Enter the items you are considering removing to build a plan.';result.append(text);
  const note=document.createElement('p');note.textContent='Counts are separate categories. Do not count the same item twice. This estimates total file bytes, not guaranteed free space on your iPhone. Optimized iCloud originals may occupy little local storage.';result.append(note);
 };
 form.addEventListener('input',update);form.addEventListener('submit',e=>{e.preventDefault();update();});update();
}
