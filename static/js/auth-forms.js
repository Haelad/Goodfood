// Проверка полей форм входа/регистрации.
//
// Пока пользователь печатает, поле нейтральное (класс is-typing, тёмно-серая рамка).
// Проверка запускается, когда ввод закончен: после паузы TYPING_DELAY
// или сразу при уходе с поля. На отправке проверяются все поля.
//
// Правила берутся из атрибутов самого поля, которые задаёт Django-форма:
// required, type="email", minlength, maxlength, pattern, data-match.
// Формы с классом no-live-valid (вход) не подсвечиваются зелёным: верность
// логина и пароля знает только сервер.

const TYPING_DELAY = 800; // мс тишины, после которых ввод считается законченным

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function compilePattern(pattern) {
  // Флаг v — как у браузерного атрибута pattern; u — запасной для старых браузеров
  for (const flags of ["v", "u"]) {
    try {
      return new RegExp(`^(?:${pattern})$`, flags);
    } catch {
      /* пробуем следующий флаг */
    }
  }
  return null;
}

// Возвращает текст ошибки или "" если значение корректно
function validate(input) {
  const value = input.value;
  const form = input.form;

  if (!value) {
    return input.required ? "Заполните это поле" : "";
  }
  if (form.classList.contains("no-live-valid")) {
    return ""; // на входе проверяем только заполненность
  }

  if (input.type === "email" && !EMAIL_RE.test(value)) {
    return "Введите корректный email, например name@mail.ru";
  }

  const min = Number(input.getAttribute("minlength"));
  if (min && value.length < min) {
    return `Минимум ${min} символов (сейчас ${value.length})`;
  }

  const max = Number(input.getAttribute("maxlength"));
  if (max && value.length > max) {
    return `Максимум ${max} символов`;
  }

  const pattern = input.getAttribute("pattern");
  if (pattern) {
    const re = compilePattern(pattern);
    if (re && !re.test(value)) {
      return "Допустимы буквы, цифры и символы _ . @ + -";
    }
  }

  if (input.dataset.match) {
    const original = document.getElementById(input.dataset.match);
    if (original && value !== original.value) {
      return "Пароли не совпадают";
    }
  }

  return "";
}

function clearMessage(input) {
  input
    .closest(".auth-field")
    ?.querySelectorAll(".auth-error")
    .forEach((el) => el.remove());
}

function showMessage(input, text) {
  clearMessage(input);
  const message = document.createElement("div");
  message.className = "auth-error";
  message.id = `${input.id}-error`;
  message.textContent = text;
  input.after(message);
  input.setAttribute("aria-describedby", message.id);
}

function setState(input, state, text = "") {
  input.classList.remove("is-typing", "is-valid", "is-invalid");
  input.removeAttribute("aria-invalid");
  clearMessage(input);

  if (state === "typing") {
    input.classList.add("is-typing");
  } else if (state === "invalid") {
    input.classList.add("is-invalid");
    input.setAttribute("aria-invalid", "true");
    showMessage(input, text);
  } else if (state === "valid") {
    input.classList.add("is-valid");
  }
}

// Итоговая проверка поля. force — проверять даже нетронутое поле (на отправке)
function check(input, { force = false } = {}) {
  clearTimeout(input._typingTimer);
  if (!force && !input.dataset.touched) return true;

  const error = validate(input);
  if (error) {
    setState(input, "invalid", error);
    return false;
  }

  const noGreen = input.form.classList.contains("no-live-valid");
  setState(input, input.value && !noGreen ? "valid" : "neutral");
  return true;
}

document.querySelectorAll(".auth-card form").forEach((form) => {
  const inputs = [...form.querySelectorAll(".auth-input")];
  if (!inputs.length) return;

  // Сообщения показываем сами, без всплывающих подсказок браузера
  form.noValidate = true;

  inputs.forEach((input) => {
    input.addEventListener("input", () => {
      input.dataset.touched = "1";
      setState(input, "typing");
      clearTimeout(input._typingTimer);
      input._typingTimer = setTimeout(() => check(input), TYPING_DELAY);

      // Изменился пароль — перепроверяем уже заполненное подтверждение
      form.querySelectorAll(`[data-match="${input.id}"]`).forEach((confirm) => {
        if (confirm.dataset.touched) {
          clearTimeout(confirm._typingTimer);
          confirm._typingTimer = setTimeout(() => check(confirm), TYPING_DELAY);
        }
      });
    });

    // Ушёл с поля — ввод закончен, проверяем сразу
    input.addEventListener("blur", () => check(input));
  });

  form.addEventListener("submit", (event) => {
    const results = inputs.map((input) => check(input, { force: true }));
    if (results.includes(false)) {
      event.preventDefault();
      inputs[results.indexOf(false)].focus();
    }
  });
});
