# Notices and fan-project status

This is an unofficial, non-commercial fan prototype. It is not affiliated with,
endorsed by, or published by Papergames / Infold Games or the creators of
*Love and Deepspace*. No game model, texture, voice, animation, UI, logo, or
screenshot is bundled in the distributable application.

The executable uses a recoloured and simplified copy of Live2D's Haruto sample
rig (`.moc3`, physics and motion data) as the motion skeleton. Review the
Live2D sample-model terms before redistributing a build:

- https://www.live2d.com/en/learn/sample/model-terms/
- https://www.live2d.com/en/learn/sample/koharu-haruto/

Rendering libraries:

- PixiJS, MIT License
- pixi-live2d-display, MIT License
- Live2D Cubism Core, subject to Live2D's SDK terms

The removable glasses are an independent accessory layer that follows the
Live2D head parameters and is animated together with the Cubism model. This is
intentional: the sample `.moc3` contains no glasses ArtMesh, and editing a
compiled `.moc3` without the original Cubism project would be misleading.
