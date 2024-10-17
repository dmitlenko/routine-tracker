function toastComponent() {
    return {
      toastOptions: {
        delay: 3000,
      },

      handleMessages(event) {
        event.detail.messages.forEach((message) => this.createToast(message));
      },

      createToast(message) {
        const toastElement = this.$refs.toastTemplate.cloneNode(true);
        toastElement.classList.remove("d-none"); // Show the new toast
        toastElement.classList.add(...message.tags.split(" "));
        toastElement.querySelector('[x-ref="toastBody"]').innerText =
          message.message;

        this.$el.appendChild(toastElement);

        const toast = new bootstrap.Toast(toastElement, this.toastOptions);
        toast.show();
      },

      init() {
        // Initialize any pre-rendered toasts on page load
        this.$el
          .querySelectorAll('.toast:not([x-ref="toastTemplate"])')
          .forEach((element) => {
            const toast = new bootstrap.Toast(element, this.toastOptions);
            toast.show();
          });
      },
    };
  }
