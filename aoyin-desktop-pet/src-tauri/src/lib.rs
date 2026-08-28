use tauri::{
    menu::{Menu, MenuItem},
    tray::TrayIconBuilder,
    Emitter, Manager, WebviewWindow,
};

#[tauri::command]
fn set_click_through(window: WebviewWindow, enabled: bool) -> Result<(), String> {
    window.set_ignore_cursor_events(enabled).map_err(|error| error.to_string())
}

#[tauri::command]
fn start_drag(window: WebviewWindow) -> Result<(), String> {
    window.start_dragging().map_err(|error| error.to_string())
}

#[tauri::command]
fn hide_window(window: WebviewWindow) -> Result<(), String> {
    window.hide().map_err(|error| error.to_string())
}

#[tauri::command]
fn quit_app(app: tauri::AppHandle) { app.exit(0); }

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let show = MenuItem::with_id(app, "show", "显示敖尹", true, None::<&str>)?;
            let glasses = MenuItem::with_id(app, "glasses", "摘下 / 戴回眼镜", true, None::<&str>)?;
            let sleep = MenuItem::with_id(app, "sleep", "休息一下", true, None::<&str>)?;
            let quit = MenuItem::with_id(app, "quit", "退出", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&show, &glasses, &sleep, &quit])?;
            TrayIconBuilder::new()
                .tooltip("敖尹 Live2D 桌宠")
                .menu(&menu)
                .on_menu_event(|app, event| match event.id.as_ref() {
                    "show" => {
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.show(); let _ = window.set_focus();
                        }
                    }
                    "glasses" | "sleep" => {
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.emit("aoyin-action", event.id.as_ref());
                        }
                    }
                    "quit" => app.exit(0),
                    _ => {}
                })
                .build(app)?;
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![set_click_through, start_drag, hide_window, quit_app])
        .run(tauri::generate_context!())
        .expect("failed to run Ao Yin desktop pet");
}
