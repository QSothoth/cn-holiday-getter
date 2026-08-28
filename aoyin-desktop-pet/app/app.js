(() => {
  'use strict';
  const embedded = window.AOYIN_EMBEDDED || null;
  const assets = embedded || {
    model: 'assets/model/aoyin/aoyin.model3.json',
    hair: 'assets/overlays/hair-crown.png',
    glasses: 'assets/overlays/glasses.png',
    face: 'assets/overlays/face-details.png',
    hand: 'assets/overlays/hand.png',
    sparkle: 'assets/overlays/sparkle.png'
  };

  const root = document.getElementById('pet-root');
  const canvas = document.getElementById('live2d-canvas');
  const speech = document.getElementById('speech');
  const menu = document.getElementById('context-menu');
  const app = new PIXI.Application({ view: canvas, resizeTo: root, backgroundAlpha: 0, antialias: true, autoDensity: true, resolution: Math.min(devicePixelRatio || 1, 2) });
  const state = { model: null, hair: null, glasses: null, face: null, hand: null, sparkle: null, glassesOn: true, animating: false, sleeping: false, clickThrough: false, pointerX: 0, pointerY: 0, action: null, bubbleTimer: 0 };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ease = t => 1 - Math.pow(1 - clamp(t, 0, 1), 3);
  const lerp = (a, b, t) => a + (b - a) * t;

  function bubble(text, ms = 2600) {
    speech.textContent = text;
    speech.classList.add('show');
    clearTimeout(state.bubbleTimer);
    state.bubbleTimer = setTimeout(() => speech.classList.remove('show'), ms);
  }

  function setParam(id, value) {
    try { state.model?.internalModel?.coreModel?.setParameterValueById(id, value); } catch (_) {}
  }

  function layout() {
    if (!state.model) return;
    const w = app.renderer.width / app.renderer.resolution;
    const h = app.renderer.height / app.renderer.resolution;
    const s = Math.min(w / state.model.width, h / state.model.height) * 0.94;
    state.model.scale.set(s);
    state.model.anchor.set(0.5, 0.5);
    state.model.position.set(w * 0.5, h * 0.515);
    const hairW = w * 0.46;
    state.hair.width = hairW; state.hair.height = hairW * (210 / 360);
    state.hair.anchor.set(0.5); state.hair.position.set(w * 0.5, h * 0.18);
    state.face.width = w * 0.245; state.face.height = state.face.width * (110 / 230);
    state.face.anchor.set(0.5); state.face.position.set(w * 0.5, h * 0.372);
    state.glasses.width = w * 0.255; state.glasses.height = state.glasses.width * (86 / 230);
    state.glasses.anchor.set(0.5); state.glasses.position.set(w * 0.5, h * 0.378);
    state.hand.width = w * 0.08; state.hand.height = state.hand.width * (86 / 72);
    state.hand.anchor.set(0.5); state.hand.visible = false;
    state.sparkle.width = w * 0.055; state.sparkle.height = state.sparkle.width;
    state.sparkle.anchor.set(0.5); state.sparkle.visible = false;
  }

  function faceBase() {
    const w = app.renderer.width / app.renderer.resolution;
    const h = app.renderer.height / app.renderer.resolution;
    return { x: w * 0.5, y: h * 0.378, hairY: h * 0.18 };
  }

  function updateOverlays(angleX, angleY, angleZ) {
    const b = faceBase();
    const w = app.renderer.width / app.renderer.resolution;
    const h = app.renderer.height / app.renderer.resolution;
    const dx = angleX * w * 0.0014;
    const dy = angleY * h * 0.0007;
    const rot = angleZ * Math.PI / 180 * 0.55;
    state.hair.position.set(w * 0.5 + dx * .75, b.hairY + dy * .42); state.hair.rotation = rot * .55;
    state.face.position.set(b.x + dx, b.y + dy); state.face.rotation = rot;
    if (!state.action && state.glassesOn) {
      state.glasses.position.set(b.x + dx, b.y + dy + h * .006); state.glasses.rotation = rot;
      state.glasses.alpha = 1; state.glasses.visible = true;
    }
  }

  async function toggleGlasses(force) {
    if (state.animating || !state.model) return;
    const puttingOn = typeof force === 'boolean' ? force : !state.glassesOn;
    if (puttingOn === state.glassesOn) return;
    state.animating = true;
    const w = app.renderer.width / app.renderer.resolution;
    const h = app.renderer.height / app.renderer.resolution;
    const b = faceBase();
    const start = performance.now();
    const duration = 1850;
    state.action = { puttingOn, start, duration };
    state.glasses.visible = true;
    state.hand.visible = true;
    state.sparkle.visible = false;
    bubble(puttingOn ? '还是戴着吧。你别一直盯着看。' : '摘下来了。这样看得更清楚？', 2800);
    return new Promise(resolve => {
      function frame(now) {
        const raw = clamp((now - start) / duration, 0, 1);
        const travel = ease(puttingOn ? 1 - raw : raw);
        const faceX = b.x; const faceY = b.y + h * .006;
        const offX = w * 0.79; const offY = h * 0.57;
        const x = lerp(faceX, offX, travel);
        const y = lerp(faceY, offY, travel) - Math.sin(travel * Math.PI) * h * .035;
        state.glasses.position.set(x, y);
        state.glasses.rotation = lerp(0, -0.26, travel);
        state.glasses.alpha = 1 - Math.max(0, (travel - .78) / .22);
        state.hand.position.set(x + w * .045, y + h * .026);
        state.hand.rotation = state.glasses.rotation * .55;
        state.hand.alpha = Math.sin(raw * Math.PI) > .05 ? Math.min(1, Math.sin(raw * Math.PI) * 2.1) : 0;
        const anticipation = Math.sin(Math.min(raw / .28, 1) * Math.PI);
        setParam('ParamAngleZ', (puttingOn ? -1 : 1) * anticipation * 6);
        setParam('ParamBodyAngleX', (puttingOn ? 1 : -1) * anticipation * 2.5);
        setParam('ParamEyeLOpen', lerp(.72, .43, anticipation));
        setParam('ParamEyeROpen', lerp(.72, .43, anticipation));
        if (raw > .62 && raw < .82) {
          state.sparkle.visible = true;
          state.sparkle.position.set(faceX + w * .105, faceY - h * .035);
          state.sparkle.alpha = Math.sin((raw - .62) / .20 * Math.PI);
          state.sparkle.rotation += .07;
        } else state.sparkle.visible = false;
        if (raw < 1) requestAnimationFrame(frame);
        else {
          state.glassesOn = puttingOn;
          state.glasses.visible = puttingOn;
          state.glasses.alpha = puttingOn ? 1 : 0;
          state.hand.visible = false; state.sparkle.visible = false;
          state.action = null; state.animating = false;
          setParam('ParamAngleZ', 0); setParam('ParamBodyAngleX', 0);
          setParam('ParamEyeLOpen', .72); setParam('ParamEyeROpen', .72);
          updateMenuLabels(); resolve();
        }
      }
      requestAnimationFrame(frame);
    });
  }

  function updateMenuLabels() {
    const btn = menu.querySelector('[data-action="glasses"]');
    if (btn) btn.textContent = state.glassesOn ? '摘下眼镜' : '戴回眼镜';
    const click = menu.querySelector('[data-action="click-through"]');
    if (click) click.textContent = state.clickThrough ? '关闭点击穿透' : '开启点击穿透';
  }

  async function invoke(command, args = {}) {
    try { return await window.__TAURI__?.core?.invoke(command, args); } catch (_) { return null; }
  }

  async function setClickThrough(enabled) {
    state.clickThrough = enabled;
    await invoke('set_click_through', { enabled });
    updateMenuLabels();
    bubble(enabled ? '点击穿透已开启。可从托盘菜单关闭。' : '现在可以碰到我了。');
  }

  function sleep() {
    state.sleeping = !state.sleeping;
    bubble(state.sleeping ? '只闭一会儿眼。别吵。' : '醒了。你还在？');
    setParam('ParamEyeLOpen', state.sleeping ? .08 : .72);
    setParam('ParamEyeROpen', state.sleeping ? .08 : .72);
    setParam('ParamAngleZ', state.sleeping ? -8 : 0);
  }

  function openMenu(ev) {
    ev.preventDefault();
    updateMenuLabels();
    menu.hidden = false;
    menu.style.left = `${Math.max(8, Math.min(ev.clientX, innerWidth - 178))}px`;
    menu.style.top = `${Math.max(8, Math.min(ev.clientY, innerHeight - 210))}px`;
  }

  async function load() {
    const model = await PIXI.live2d.Live2DModel.from(assets.model, { autoInteract: false });
    state.model = model;
    app.stage.addChild(model);
    state.hair = PIXI.Sprite.from(assets.hair);
    state.face = PIXI.Sprite.from(assets.face);
    state.glasses = PIXI.Sprite.from(assets.glasses);
    state.hand = PIXI.Sprite.from(assets.hand);
    state.sparkle = PIXI.Sprite.from(assets.sparkle);
    app.stage.addChild(state.hair, state.face, state.glasses, state.hand, state.sparkle);
    layout();
    setParam('ParamEyeLOpen', .72); setParam('ParamEyeROpen', .72); setParam('ParamMouthOpenY', 0);
    try { await model.motion('Idle', 0); } catch (_) {}
    bubble('……总算安静下来了。', 2200);
    window.__AOYIN_READY__ = true;
  }

  let phase = 0;
  app.ticker.add(delta => {
    if (!state.model) return;
    phase += delta / 60;
    const w = app.renderer.width / app.renderer.resolution;
    const h = app.renderer.height / app.renderer.resolution;
    const targetX = clamp(state.pointerX / Math.max(w, 1), -1, 1) * 10;
    const targetY = clamp(state.pointerY / Math.max(h, 1), -1, 1) * -6;
    const angleX = state.sleeping ? -4 : targetX + Math.sin(phase * .45) * .6;
    const angleY = state.sleeping ? -5 : targetY + Math.sin(phase * .31) * .35;
    const angleZ = state.sleeping ? -8 : Math.sin(phase * .24) * .8;
    if (!state.animating) {
      setParam('ParamAngleX', angleX); setParam('ParamAngleY', angleY); setParam('ParamAngleZ', angleZ);
      setParam('ParamBodyAngleX', Math.sin(phase * .35) * .7);
      setParam('ParamBreath', (Math.sin(phase * 1.7) + 1) / 2);
      if (!state.sleeping) { setParam('ParamEyeLOpen', .72); setParam('ParamEyeROpen', .72); }
    }
    updateOverlays(angleX, angleY, state.animating ? 0 : angleZ);
  }, undefined, PIXI.UPDATE_PRIORITY.LOW);

  root.addEventListener('pointermove', ev => { state.pointerX = ev.clientX - innerWidth / 2; state.pointerY = ev.clientY - innerHeight / 2; });
  root.addEventListener('pointerleave', () => { state.pointerX = 0; state.pointerY = 0; });
  root.addEventListener('dblclick', ev => {
    const nx = ev.clientX / innerWidth, ny = ev.clientY / innerHeight;
    if (nx > .30 && nx < .70 && ny > .25 && ny < .49) toggleGlasses();
    else bubble('别戳。有什么事直接说。');
  });
  root.addEventListener('contextmenu', openMenu);
  document.addEventListener('pointerdown', ev => { if (!menu.contains(ev.target)) menu.hidden = true; });
  menu.addEventListener('click', async ev => {
    const action = ev.target?.dataset?.action; if (!action) return; menu.hidden = true;
    if (action === 'glasses') toggleGlasses();
    if (action === 'sleep') sleep();
    if (action === 'click-through') setClickThrough(!state.clickThrough);
    if (action === 'hide') await invoke('hide_window');
    if (action === 'quit') await invoke('quit_app');
  });
  addEventListener('resize', layout);
  addEventListener('keydown', ev => {
    if (ev.key.toLowerCase() === 'g') toggleGlasses();
    if (ev.key.toLowerCase() === 'z') sleep();
    if (ev.key === 'Escape') menu.hidden = true;
  });

  let dragStart = null;
  root.addEventListener('pointerdown', ev => { if (ev.button === 0) dragStart = { x: ev.clientX, y: ev.clientY, t: performance.now() }; });
  root.addEventListener('pointerup', async ev => {
    if (!dragStart) return;
    const dist = Math.hypot(ev.clientX - dragStart.x, ev.clientY - dragStart.y);
    const held = performance.now() - dragStart.t; dragStart = null;
    if (dist > 8 || held > 230) await invoke('start_drag');
  });

  if (window.__TAURI__?.event?.listen) {
    window.__TAURI__.event.listen('aoyin-action', ev => {
      if (ev.payload === 'glasses') toggleGlasses();
      if (ev.payload === 'sleep') sleep();
    });
  }

  load().catch(err => {
    console.error(err);
    bubble(`Live2D 模型加载失败：${err?.message || err}`, 10000);
    window.__AOYIN_ERROR__ = String(err);
  });
  window.AoYinPet = { toggleGlasses, sleep, state };
})();
