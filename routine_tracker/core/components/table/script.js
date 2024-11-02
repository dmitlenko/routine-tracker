(() => {
  const tbody = document.querySelector(".table tbody");

  new MutationObserver((mutationList) => {
    for (const mutation of mutationList) {
      if (mutation.type === "childList") {
        const emptyMessageRow = document.querySelector(".empty-message-row");

        if (tbody.children.length === 1 && tbody.children[0].isSameNode(emptyMessageRow)) {
          emptyMessageRow.classList.remove("d-none");
        } else {
          emptyMessageRow.classList.add("d-none");
        }
      }
    }
  }).observe(tbody, { childList: true });
})();
