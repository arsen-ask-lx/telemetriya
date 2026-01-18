// .opencode/plugin/notification-win.js
// Уведомление в Windows через BurntToast при событии session.idle
// + защита от дублей + нормальная русская кодировка + без всплывающего PowerShell-окна

export const NotificationWin = async ({ $ }) => {
  let lastNotificationTime = 0;

  return {
    event: async ({ event }) => {
      if (event?.type !== "session.idle") return;

      const now = Date.now();
      if (now - lastNotificationTime < 2000) return; // антидубль 2 сек
      lastNotificationTime = now;

      // Текст уведомления
      const title = "opencode";
      const body = "Готово";

      // PowerShell-скрипт одной строкой (важно для кавычек и -Command)
      // 1) Пытаемся импортировать BurntToast
      // 2) Показываем уведомление
      // 3) Ничего не открываем (WindowStyle Hidden)
      const ps = `
        $ErrorActionPreference = 'SilentlyContinue';
        Import-Module BurntToast;
        New-BurntToastNotification -Text '${escapePs(title)}','${escapePs(body)}' | Out-Null;
      `.trim().replace(/\s+/g, " ");

      try {
        await $`powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command ${ps}`;
      } catch (_) {
        // не ломаем агента, если что-то не так
      }
    },
  };
};

// экранирование одинарных кавычек для PowerShell строк '...'
function escapePs(s) {
  return String(s).replace(/'/g, "''");
}
