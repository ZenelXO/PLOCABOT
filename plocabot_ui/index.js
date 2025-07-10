let lastUserOption = 1; 
const input = document.getElementById('user-input');
const chat = document.getElementById('chat');
let selectedEnvironment = null;
let idConversacionActiva = null;
let userId = localStorage.getItem("userId");
const userMenu = document.getElementById('userMenu');
const userProfile = document.querySelector('.userProfile');
const lightthemeOption = document.getElementById("light");
const darkthemeOption = document.getElementById("dark");
const voiceOptionPablo = document.getElementById("pablo");
const voiceOptionLaura = document.getElementById("laura");
let pabloVoice = null;

window.speechSynthesis.onvoiceschanged = () => {
  const voices = speechSynthesis.getVoices();
  pabloVoice = voices.find(voice => voice.name.includes("Laura"));
};

document.addEventListener("DOMContentLoaded", () => {
  localStorage.setItem("voiceMode", false)
  try {
    const nameInitialElem = document.getElementById("nameInitial");
    nameInitialElem.innerText = userId.charAt(0).toUpperCase();
  } catch (error) {
    console.warn("Elemento #nameInitial no encontrado o error al asignar texto:", error);
  }
  idConversacionActiva = null;
  firstInteraction();
  cargarHistorialReal();
});

function logErrorPersistently(error) {
  const logs = JSON.parse(localStorage.getItem("errorLogs") || "[]");

  const errorInfo = {
    time: new Date().toISOString(),
    message: error.message || error.toString(),
    stack: error.stack || "No stack trace available"
  };

  logs.push(errorInfo);
  localStorage.setItem("errorLogs", JSON.stringify(logs));

  console.error("🧨 (Guardado) →", errorInfo.message);
  console.error(errorInfo.stack);
}

window.addEventListener("load", () => {
  const logs = JSON.parse(localStorage.getItem("errorLogs") || "[]");
  if (logs.length > 0) {
    console.warn("📝 Errores guardados de sesiones anteriores:");
    logs.forEach(log => {
      console.warn(`[${log.time}] ${log.message}`);
      console.warn(log.stack);
    });
    // localStorage.removeItem("errorLogs");
  }
});

function toggleUserMenu() {
  if (userMenu.style.display === 'block') {
    userMenu.style.display = 'none';
  } else {
    userMenu.style.display = 'block';
  }
}

function logOut() {
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
    window.location.href = "login.html";
}

userProfile.addEventListener('click', function(e) {
  e.stopPropagation();
  toggleUserMenu();
});

document.addEventListener('click', function(e) {
  if (
    userMenu.style.display === 'block' &&
    !userMenu.contains(e.target) &&
    !userProfile.contains(e.target)
  ) {
    userMenu.style.display = 'none';
  }
});

//MODO CLARO---------------------------------------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  lightthemeOption.addEventListener("click", function() {
     localStorage.setItem("Theme", "bright");
    document.querySelectorAll('.message.bot .bubble').forEach(bubble => {
      bubble.style.backgroundColor = "#f0f0f0";
      bubble.style.color = "#000000";
    });

    document.querySelectorAll('.message.user .bubble').forEach(bubble => {
      bubble.style.backgroundColor = "#e0e0e0";
      bubble.style.color = "#000000";
    });

    document.body.style.background = "linear-gradient(180deg, #f4f7fb, #ffffff)";
    document.querySelector("header").style.background = "linear-gradient(270deg, #e3f2fd, #bbdefb, #90caf9)";
    document.querySelector("main").style.backgroundColor = "#FFFFFF";
    document.querySelector("#historialContainer").style.background = "linear-gradient(0deg, #e3f2fd, #bbdefb, #90caf9)";
    document.getElementById("historialContainer").style.color = "black";
    document.getElementById("user-input").style.backgroundColor = "#e6e6e6";
    document.getElementById("user-input").style.color = "black";
    document.getElementById("newChatMain").style.color = "black";
    document.getElementById("newChat").style.color = "black";
    document.getElementById("searchicon").style.color = "black";
    document.querySelector(".buttonsExtra").style.background = "#e6e6e6";
  });

  //MODO OSCURO---------------------------------------------------------------------------------------------------------------
  darkthemeOption.addEventListener("click", function () {
    localStorage.setItem("Theme", "dark");

    document.body.style.background = "linear-gradient(180deg, #1a1a1a, #121212)";
    document.querySelector("header").style.background = "linear-gradient(90deg, #1e1e1e, #2c2c2c, #1e1e1e)";
    document.querySelector("main").style.backgroundColor = "#121212";

    document.getElementById("chat-form").style.backgroundColor = "#1e1e1e";
    document.getElementById("chat-form").style.color = "#e0e0e0";
    document.getElementById("user-input").style.color = "#ffffff";
    document.getElementById("user-input").style.backgroundColor = "#2a2a2a";

    document.querySelector("#historialContainer").style.background = "linear-gradient(210deg, #1e1e1e, #2c2c2c, #1e1e1e)";
    document.getElementById("historialContainer").style.color = "#f0f0f0";
    document.getElementById("newChatMain").style.color = "#f0f0f0";
    document.getElementById("newChat").style.color = "#f0f0f0";
    document.getElementById("searchicon").style.color = "#f0f0f0";
    document.querySelector(".buttonsExtra").style.background = "#1e1e1e";

    document.querySelectorAll('.message.bot .bubble').forEach(bubble => {
      bubble.style.backgroundColor = "#2e2e2e";
      bubble.style.color = "#f0f0f0";
    });

    document.querySelectorAll('.message.user .bubble').forEach(bubble => {
      bubble.style.backgroundColor = "#254d37";
      bubble.style.color = "#f0f0f0";
    });

});


  voiceOptionPablo.addEventListener("click", function() {
    const voices = speechSynthesis.getVoices();
    pabloVoice = voices.find(voice => voice.name.includes("Pablo"));
    alert("Has cambiado la voz del chatbot a la de Pablo con éxito.");
  });

  voiceOptionLaura.addEventListener("click", function() {
    const voices = speechSynthesis.getVoices();
    pabloVoice = voices.find(voice => voice.name.includes("Laura"));
    alert("Has cambiado la voz del chatbot a la de Laura con éxito.");
  });

  document.getElementById('theme-btn').addEventListener('click', () => {
    const menu = document.getElementById('theme-dropdown');
    menu.classList.toggle('hidden');
    
    document.getElementById('language-dropdown').classList.add('hidden');
    document.getElementById('voice-dropdown').classList.add('hidden');
  });

  document.getElementById('voice-btn').addEventListener('click', () => {
    const menu = document.getElementById('voice-dropdown');
    menu.classList.toggle('hidden');
    
    document.getElementById('theme-dropdown').classList.add('hidden');
    document.getElementById('language-dropdown').classList.add('hidden');
  });

  document.getElementById('language-btn').addEventListener('click', () => {
    const menu = document.getElementById('language-dropdown');
    menu.classList.toggle('hidden');
    
    document.getElementById('theme-dropdown').classList.add('hidden');
    document.getElementById('voice-dropdown').classList.add('hidden');
  });
});

//MENSAJES POR AUDIO-----------------------------------------------------------------------------------------------------------
let mediaRecorder;
let audioChunks = [];
let audioBlob;

async function voice_stop_recording(event) {
  event.preventDefault();

  startBtn.style.display = "block";
  stopBtn.classList.add("hidden");

  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
}

async function voice_recording(event) {
  event.preventDefault();

  try {
    // Listar dispositivos
    const devices = await navigator.mediaDevices.enumerateDevices();
    const hasAudioInput = devices.some(device => device.kind === "audioinput");

    if (!hasAudioInput) {
      alert("No se detectó ningún micrófono conectado. Por favor conecta uno para usar esta función.");
      return;
    }

    // Si hay micrófono, pedir permiso y grabar
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    startBtn.style.display = "none";
    stopBtn.classList.remove("hidden");

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      audioBlob = new Blob(audioChunks, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      fetch("http://127.0.0.1:5000/audio-to-text", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          input.value = data.text;
          document.getElementById("chat-form").requestSubmit();
        })
        .catch((error) => {
          logErrorPersistently(error)
          console.error("Error enviando audio:", error);
        });
    };

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;

  } catch (error) {
    // Aquí puede ser que el usuario no dio permiso o algún otro error
    alert("No se pudo acceder al micrófono: " + error.message);
    console.error(error);
    logErrorPersistently(error)
  }
}

startBtn.addEventListener("click", async (event) => {
  try {
    await voice_recording(event);
  } catch (err) {
    console.error("Error en voice_recording:", err);
    logErrorPersistently(err)
  }
});

stopBtn.addEventListener("click", async (event) => {
  try {
    await voice_stop_recording(event);
  } catch (err) {
    console.error("Error en voice_recording:", err);
    logErrorPersistently(err)
  }
});

function firstInteraction() {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', 'bot');

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');

  const text = `<span data-i18n = "intro1">
    🌟 ¡Hola! Soy </span><strong>${CONFIG.botName}</strong> 🤖<br>
    <div <span data-i18n = "intro2">>Antes de comenzar, por favor elige qué te gustaría hacer:</div><br><br>
    <button class="option-btn" onclick="handleOptionClick('1')"><span data-i18n = "Option1">1: Tomar el control manual de una cámara</button><br>
    <button class="option-btn" onclick="handleOptionClick('2')"><span data-i18n = "Option2">2: Obtener información sobre detecciones</button>
  `;

  bubble.innerHTML = text;
  messageDiv.appendChild(bubble);
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;
}

// Envío del formulario
document.getElementById('chat-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const message = input.value.trim();
  if (message === '') {
    alert("Debes introducir un mensaje, para que sea enviado.");
    return;
  }

  appendMessage('user', message);
  input.value = '';

  appendThinkingMessage();

  try {
    const botResponse = await Promise.race([
      getBotResponse(message),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("timeout")), 120000)
      )
    ]);
    removeThinkingMessage();
    appendMessage('bot', botResponse);
    //Aquí hacemos que si la variable de voiceMode esta a True, se escuche el mensaje:
    if (localStorage.getItem("voiceMode") === "true") {
      const utterance = new SpeechSynthesisUtterance(botResponse);
      if (pabloVoice) {
        utterance.voice = pabloVoice;
      }
      utterance.rate = 1.5;
      utterance.pitch = 1.1;
      speechSynthesis.speak(utterance);
    }
  } catch (error) {
    removeThinkingMessage();
    if (error.message === "timeout") {
      appendMessage('bot', "⏳ El sistema está tardando más de lo esperado. Por favor, intenta de nuevo en unos momentos.");
    } else {
      appendMessage('bot', "❌ Ocurrió un error al obtener la respuesta. Inténtalo más tarde.");
    }
  }
});

// Lógica simple para la respuesta del bot
async function getBotResponse(input) {
    input = input.toLowerCase();
    
    if (lastUserOption !== 1) {
        if (lastUserOption === 2) {
            // Comprobamos si el mensaje del usuario coincide con un entorno
            allEnvironments = await environmentsGetter();
            let selectedEnvironment = null;
            let idConversacionActiva = null;
    
            for (let i of allEnvironments) {
                for (const [id, data] of Object.entries(i)) {
                    if (data.name && data.name.toLowerCase() === input.toLowerCase()) {
                        selectedEnvironment = id;
                        selectedProduct = data.product_id
                        selectedModel = data.model_name
                        lastUserOption = 0;
                        
                        environmentSetter(selectedEnvironment, selectedProduct, selectedModel);
                        return `
                            <div class="entorno-confirm">
                                <h3>🌍 Entorno seleccionado: <strong>${data.name}</strong> ✅</h3>
                                <p>A continuación te doy algunos tips para sacarle el máximo partido:</p>
                                <li>💬 Puedes escribir en español o inglés si no te entiendo.</li>
                                <li>📍 Usa el nombre exacto del lugar tal como aparece en “<strong>Lugares</strong>”.</li>
                                <li>🔎 Escribe <strong><code>Lugares</code></strong> para ver todos los sitios disponibles.</li>
                                <li>📊 Escribe <strong><code>Detecciones</code></strong> para ver los tipos que puedo mostrarte.</li>
                                <p class="conclusion">🚀 ¡Hazme tu primera pregunta cuando quieras!</p>
                            </div>
                            `;
                    }
                }
            }
            return `❌ El entorno no es válido. Por favor, elige un entorno de la lista para continuar.`;
        } else if (input.includes('lugares')) {
          allPlaces = await placesGetter();
          allImagesFromPlaces = await placesImagesGetter();
          
          let bubbleContent = '🗺️ Estos son todos los lugares de los que puedes pedirme información:\n\n';
          
          for (const place of allPlaces) {
              const imageUrl = allImagesFromPlaces[place];
              
              if (imageUrl) {
                  const placeContainer = document.createElement('div');
                  placeContainer.classList.add('picUrlContainer');
                  
                  const placeName = document.createElement('div');
                  placeName.classList.add('place-name');
                  placeName.innerText = `🔹 ${place}:`;
                  
                  const imageContainer = document.createElement('div');
                  imageContainer.classList.add('image-container');
                  
                  const image = document.createElement('img');
                  image.src = imageUrl;
                  image.alt = place;
                  image.classList.add('place-image');
                  
                  imageContainer.appendChild(image);
                  placeContainer.appendChild(placeName);
                  placeContainer.appendChild(imageContainer);
                  
                  bubbleContent += placeName.outerHTML + imageContainer.outerHTML + "\n\n";
              }
          }
          const placesAnswer = `<div class="entorno-confirm">${bubbleContent}</div>`;

          if (idConversacionActiva) {
              fetch("http://127.0.0.1:5000/guardarMensaje", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                      conversationId: idConversacionActiva,
                      sender: "bot",
                      text: placesAnswer
                  })
              });
          }

          return placesAnswer;

        } else if (input === '1'){
            return '<span data-i18n = "environment4">🚧 ¡Ups! Esta opción aún está en desarrollo.</span>🚧<br><span data-i18n = "environment5">Muy pronto estará disponible para que puedas usarla.</span><br><br><span data-i18n = "environment6">¡Gracias por tu paciencia! 😊</span>';
        } else if (input === '2') {
            let prettyEnvironmentNames = `<span data-i18n = "environment1">👋 ¡Hola! Antes de empezar, necesitas elegir un entorno donde quieras trabajar.</span><br><br>`;
            prettyEnvironmentNames += `<span data-i18n = "environment2">📋 Aquí tienes la lista de entornos disponibles:</span><br><br>`;

            allEnvironments = await environmentsGetter();
            for (const i of allEnvironments) {
                for (const [id, data] of Object.entries(i)) {
                prettyEnvironmentNames += `<button class="option-btn" onclick="handleOptionClick('${data.name}')">${data.name}</button><br>`;
                }
            }

            prettyEnvironmentNames += `<br><span data-i18n = "environment3">✍️ O haz clic sobre el nombre del entorno que te interesa.</span>`;
            lastUserOption = 2;
            return prettyEnvironmentNames;
        } else {
            model_answer = await start_conversation(input);
            return model_answer;
        }
    } else {
        if (input === '1'){
            return '<span data-i18n = "environment4">🚧 ¡Ups! Esta opción aún está en desarrollo.</span>🚧<br><span data-i18n = "environment5">Muy pronto estará disponible para que puedas usarla.</span><br><br><span data-i18n = "environment6">¡Gracias por tu paciencia! 😊</span>';
        } else if (input === '2') {
            let prettyEnvironmentNames = `<span data-i18n = "environment1">👋 ¡Hola! Antes de empezar, necesitas elegir un entorno donde quieras trabajar.</span><br><br>`;
            prettyEnvironmentNames += `<span data-i18n = "environment2">📋 Aquí tienes la lista de entornos disponibles:</span><br><br>`;

            allEnvironments = await environmentsGetter();
            for (const i of allEnvironments) {
                for (const [id, data] of Object.entries(i)) {
                prettyEnvironmentNames += `<button class="option-btn" onclick="handleOptionClick('${data.name}')">${data.name}</button><br>`;
                }
            }

            prettyEnvironmentNames += `<br><span data-i18n = "environment3">✍️ O haz clic sobre el nombre del entorno que te interesa.</span>`;
            lastUserOption = 2;
            return prettyEnvironmentNames;
        } else {
            return `<span data-i18n = "environmentError">❌ Opción no válida. Por favor, elige una opción de la lista para continuar.</span>`;
        }
    }
    
}

// Agregar mensaje con animación y salto de línea
function appendMessage(sender, text) {
  const theme = localStorage.getItem("Theme");

  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  bubble.innerHTML = text.replace(/\n/g, '<br>');

  if (theme === "dark") {
    if (sender === "bot") {
      bubble.style.backgroundColor = "#2e2e2e";
      bubble.style.color = "#f0f0f0";
    }
    else if (sender === "user") {
      bubble.style.backgroundColor = "#2e2e2e";
      bubble.style.color = "#f0f0f0";
    }
  }

  if (theme === "bright") {
    if (sender === "bot") {
      bubble.style.backgroundColor = "#f5f5f5";
      bubble.style.color = "#333";
    }
    else if (sender === "user") {
      bubble.style.backgroundColor = "#DCF8C6";
      bubble.style.color = "#222";
    }
  }

  messageDiv.appendChild(bubble);
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;
}


// Mostrar burbuja de "Pensando..." animada
function appendThinkingMessage() {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', 'bot');
  messageDiv.id = "thinking-message";
  if(localStorage.getItem("Theme" === "dark")){
    messageDiv.style.backgroundColor = "#2e2e2e";
    messageDiv.style.color = "#f0f0f0";
  }
  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  bubble.innerHTML = "<span class='dots'><span>.</span><span>.</span><span>.</span></span>";

  messageDiv.appendChild(bubble);
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;
}

function removeThinkingMessage() {
  const thinkingMessage = document.getElementById("thinking-message");
  if (thinkingMessage) thinkingMessage.remove();
}

function handleOptionClick(text) {
  appendMessage('user', text);
  input.value = '';
  appendThinkingMessage();

  getBotResponse(text).then(botResponse => {
    removeThinkingMessage();
    appendMessage('bot', botResponse);
    updateLanguage(localStorage.getItem("lang") || "es");
  });
}

function newConversation() {
  chat.innerHTML = '';
  idConversacionActiva = null;
  lastUserOption = 1;
  firstInteraction();
  cargarHistorialReal();
}


//-------------------------------------------------------------------------------------
async function placesGetter() {
    const respuesta = await fetch("http://127.0.0.1:5000/placesGetter", {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    respuestaAPI = await respuesta.json()

    return respuestaAPI;
}

async function placesImagesGetter() {
    const respuesta = await fetch("http://127.0.0.1:5000/placesImagesGetter", {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    respuestaAPI = await respuesta.json()

    return respuestaAPI;
}

async function detectionsGetter() {
    const respuesta = await fetch("http://127.0.0.1:5000/detectionsGetter", {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    respuestaAPI = await respuesta.json()

    return respuestaAPI;
}

async function environmentSetter(selectedEnvironment, selectedProduct, selectedModel) {
    const respuesta = await fetch("http://127.0.0.1:5000/environmentSetter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entorno: selectedEnvironment , producto : selectedProduct, modelo : selectedModel})
    });

    const respuestaAPI = await respuesta.json();
    return respuestaAPI;
}

async function environmentsGetter(){
    const respuesta = await fetch("http://127.0.0.1:5000/environmentsGetter", {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    const respuestaAPI = await respuesta.json();
    return respuestaAPI;
}

async function start_conversation(input) {
    const pregunta = input;

    const respuesta = await fetch("http://127.0.0.1:5000/new_chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "mensaje": pregunta })
    });
    const respuestaAPI = await respuesta.json();
    return respuestaAPI.respuesta;
}

// -------------------- FUNCIONALIDAD DE HISTORIAL --------------------
async function cargarHistorialReal() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/historial/${userId}`);
    const data = await response.json();
    const historialContainer = document.getElementById("historial-list");
    if (!historialContainer) return;

    historialContainer.innerHTML = '';

    if (data.length === 0) {
      historialContainer.innerHTML = "<p class='dateHistorial'>No hay conversaciones</p>";
      return;
    }

    // Lógica para filtrar y agrupar conversaciones por fecha
    const hoy = new Date();
    const sieteDias = new Date(hoy);
    sieteDias.setDate(hoy.getDate() - 7);
    const treintaDias = new Date(hoy);
    treintaDias.setDate(hoy.getDate() - 30);

    data.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    const lang = localStorage.getItem("lang") || "es";

    const secciones = {
      [translations[lang].today]: [],
      [translations[lang].last7]: [],
      [translations[lang].last30]: [],
      [translations[lang].older]: []
    };

    data.forEach(conv => {
      const fechaConv = new Date(conv.createdAt);
      const titulo = conv.messages.length > 0 ? conv.messages[0].text.slice(0, 30) : translations[lang].no_messages;

      const convHTML = `
        <div class="textHistorialContainer">
          <p class="textHistorial" onclick="mostrarConversacion('${conv._id}')" id="${conv._id}">
            ${titulo}
            <span class="fa-solid fa-trash" onclick="removeConversation('${conv._id}')"></span>
          </p>
        </div>
      `;

      if (fechaConv.toDateString() === hoy.toDateString()) {
        secciones[translations[lang].today].push(convHTML);
      } else if (fechaConv > sieteDias) {
        secciones[translations[lang].last7].push(convHTML);
      } else if (fechaConv > treintaDias) {
        secciones[translations[lang].last30].push(convHTML);
      } else {
        secciones[translations[lang].older].push(convHTML);
      }
    });


    for (const [nombre, conversaciones] of Object.entries(secciones)) {
      if (conversaciones.length > 0) {
        historialContainer.innerHTML += `<p class='dateHistorial'>${nombre}</p>`;
        conversaciones.forEach(html => historialContainer.innerHTML += html);
      }
    }

  } catch (error) {
    console.error("Error cargando historial:", error);
  }
}


async function mostrarConversacion(id) {
  try {
    const res = await fetch(`http://127.0.0.1:5000/conversacion/${id}`);
    const data = await res.json();

    if (!data || !data.messages) {
      alert("❌ No se pudo cargar la conversación.");
      return;
    }

    chat.innerHTML = "";
    idConversacionActiva = id;

    document.querySelectorAll(".textHistorial").forEach(elem => {
      elem.style.removeProperty("background-color");
      elem.style.removeProperty("color");
    });

    const elementoActivo = document.getElementById(id);
    if (elementoActivo) {
      elementoActivo.style.backgroundColor = "#ffffff33";
      elementoActivo.style.borderRadius = "5px";
    }
    
    // Ordenar mensajes por fecha (por si vienen desordenados)
    data.messages.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    data.messages.forEach(msg => {
      appendMessage(msg.sender, msg.text);
    });

    // Restaurar opción elegida
    const ultimaPregunta = data.messages.findLast(m => m.sender === 'user');
    if (ultimaPregunta) {
      if (ultimaPregunta.text === '1') {
        lastUserOption = 1;
      } else if (ultimaPregunta.text === '2') {
        lastUserOption = 2;
      } else {
        lastUserOption = 0;
      }
    }

    // Restaurar entorno si estaba seleccionado
    const entornoMsg = data.messages.find(m => m.sender === 'bot' && m.text.includes("🌍 Entorno seleccionado"));
    if (entornoMsg) {
      const match = entornoMsg.text.match(/<strong>(.*?)<\/strong>/);
      if (match && match[1]) {
        const nombreEntorno = match[1].trim().toLowerCase();
        environmentsGetter().then(allEnvs => {
          for (let i of allEnvs) {
            for (const [id, data] of Object.entries(i)) {
              if (data.name.toLowerCase() === nombreEntorno) {
                selectedEnvironment = id;
                selectedProduct = data.product_id;
                selectedModel = data.model_name;
                environmentSetter(selectedEnvironment, selectedProduct, selectedModel);
              }
            }
          }
        });
      }
    }

  } catch (error) {
    console.error("Error al cargar conversación:", error);
    alert("❌ Ocurrió un error al recuperar la conversación.");
  }
}

async function start_conversation(input) {
  const respuesta = await fetch("http://127.0.0.1:5000/new_chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      mensaje: input,
      conversationId: idConversacionActiva,
      userId : userId
    })
  });

  const respuestaAPI = await respuesta.json();

  if (respuestaAPI.conversationId) {
    idConversacionActiva = respuestaAPI.conversationId;
  }

  return respuestaAPI.respuesta;
}

async function removeConversation(convId) {
  const confirmacion = window.confirm("¿Está seguro de que desea eliminar esta conversación?");
  if (confirmacion){
    const respuesta = await fetch(`http://127.0.0.1:5000/eliminarConversacion/${convId}`, {
      method: "DELETE"
    });
    window.location.reload();
  }
}

async function closeHistorial() {
  const historial = document.getElementsByClassName("historialContainer")[0];
  const openButton = document.getElementById("openHistorial");

  historial.classList.add("oculto");

  setTimeout(() => {
    historial.style.display = "none";
    openButton.classList.remove("visible");
    openButton.style.display = "flex";
    void openButton.offsetWidth;
    openButton.classList.add("visible");
  }, 400);
}


async function openHistorial() {
  const historial = document.getElementsByClassName("historialContainer")[0];
  const openButton = document.getElementById("openHistorial");

  historial.style.display = "flex";
  openButton.style.display = "none";

  void historial.offsetWidth;

  historial.classList.remove("oculto");
}
