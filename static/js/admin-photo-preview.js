// Превью фото в админке до сохранения.
//
// Виджет unfold (clearable_file_input.html) показывает миниатюру только уже
// сохранённого файла. Здесь при выборе нового файла миниатюра подменяется
// локальной картинкой (или создаётся, если записи ещё нет), а в поле
// с путём подставляется имя выбранного файла.

const PATH_FIELD = "input[type='text'][disabled]";

// unfold на change перезаписывает атрибут value поля пути (а при отмене
// выбора — пустой строкой), поэтому исходный путь запоминаем при загрузке
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(PATH_FIELD).forEach((field) => {
    field.dataset.savedValue = field.value;
  });
});

document.addEventListener("change", (event) => {
  const input = event.target;
  if (!input.matches('input[type="file"][accept="image/*"]')) return;

  // Обёртка виджета — блок, где лежит неактивное поле с путём к файлу
  const wrapper = input.closest(`div:has(> label ${PATH_FIELD})`);
  if (!wrapper) return;

  const file = input.files[0];
  const preview = getPreview(wrapper);
  const pathField = wrapper.querySelector(PATH_FIELD);

  if (!file || !file.type.startsWith("image/")) {
    preview.restore();
    // Обработчик unfold уже отработал (он висит на самом input), перезаписываем
    const saved = pathField.dataset.savedValue ?? "";
    pathField.setAttribute("value", saved);
    pathField.value = saved;
    return;
  }

  preview.show(file);
  pathField.value = file.name;
});

function getPreview(wrapper) {
  // Миниатюра unfold стоит прямо перед обёрткой: <div class="mb-4 max-w-48"><a><img>
  let box = wrapper.previousElementSibling;
  if (!box?.matches(".max-w-48")) {
    box = document.createElement("div");
    box.className = "mb-4 max-w-48";
    box.hidden = true;
    box.innerHTML = '<img alt="Превью фото" class="block rounded-default">';
    wrapper.before(box);
  }

  const img = box.querySelector("img");
  img.dataset.savedSrc ??= img.getAttribute("src") || "";

  return {
    show(file) {
      if (img.src.startsWith("blob:")) URL.revokeObjectURL(img.src);
      img.src = URL.createObjectURL(file);
      box.hidden = false;
    },
    // Выбор отменён — возвращаем сохранённое фото или прячем превью
    restore() {
      if (img.src.startsWith("blob:")) URL.revokeObjectURL(img.src);
      if (img.dataset.savedSrc) {
        img.src = img.dataset.savedSrc;
      } else {
        img.removeAttribute("src");
        box.hidden = true;
      }
    },
  };
}
