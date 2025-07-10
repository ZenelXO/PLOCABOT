const translations = {
  es: {
    theme: "Tema",
    dark: "Oscuro",
    light: "Claro",
    voice: "Voz",
    pablo: "Pablo",
    laura: "Laura",
    language: "Idioma",
    logout: "Cerrar sesión",
    history: "Historial",
    new_conversation: "Nueva conversación",
    input_placeholder: "Escribe tu mensaje aquí...",
    send: "Enviar",
    today: "Hoy",
    last7: "Últimos 7 días",
    last30: "Últimos 30 días",
    older: "Más antiguas",
    no_messages: "(sin mensajes)",
    Option1: "1: Tomar el control manual de una cámara",
    Option2: "2: Obtener información sobre detecciones",
    intro1: `🌟 ¡Hola! Soy `,
    intro2: "Antes de comenzar, por favor elige qué te gustaría hacer:",
    environment1: "👋 ¡Hola! Antes de empezar, necesitas elegir un entorno donde quieras trabajar.",
    environment2: "📋 Aquí tienes la lista de entornos disponibles:",
    environment3: "✍️ O haz clic sobre el nombre del entorno que te interesa.",
    environmentError: "❌ Opción no válida. Por favor, elige una opción de la lista para continuar.",
    environment4: `🚧 ¡Ups! Esta opción aún está en desarrollo.`,
    environment5: "Muy pronto estará disponible para que puedas usarla.",
    environment6: "¡Gracias por tu paciencia! 😊"
  },
  en: {
    theme: "Theme",
    dark: "Dark",
    light: "Light",
    voice: "Voice",
    pablo: "Pablo",
    laura: "Laura",
    language: "Language",
    logout: "Log out",
    history: "History",
    new_conversation: "New conversation",
    input_placeholder: "Type your message here...",
    send: "Send",
    today: "Today",
    last7: "Last 7 days",
    last30: "Last 30 days",
    older: "Older",
    no_messages: "(no messages)",
    Option1: "1: Take manual control of a camera",
    Option2: "2: Obtain information about system detections",
    intro1: `🌟Hi! I am `,
    intro2: "Before we start, please choose what you would like to do:",
    environment1: "👋 Hi! Now, you need to choose the environment you prefer to work with.",
    environment2: "📋 Here you have the list of all the avaliable environments:",
    environment3: "✍️ Or just click on the name of the environment you are interested.",
    environmentError: "❌ That is not a valid option. Please, choose one of the options from the list to continue.",
    environment4: "🚧 Whoops! This option is still on development.",
    environment5: "Very soon it will be available for usage.",
    environment6: "Thanks for your patience! 😊"
  }
};

function updateLanguage(lang) {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (translations[lang] && translations[lang][key]) {
      el.textContent = translations[lang][key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (translations[lang] && translations[lang][key]) {
      el.placeholder = translations[lang][key];
    }
  });
}

function initLanguageSelector() {
  const savedLang = localStorage.getItem("lang") || "es";
  updateLanguage(savedLang);

  document.querySelectorAll("#language-dropdown li a").forEach(link => {
    link.addEventListener("click", e => {
      const lang = link.textContent.toLowerCase().startsWith("en") ? "en" : "es";
      localStorage.setItem("lang", lang);
      updateLanguage(lang);
      cargarHistorialReal();
    });
  });
}

window.addEventListener("DOMContentLoaded", initLanguageSelector);
