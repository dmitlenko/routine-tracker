/**
 * @typedef {{ tags: string, message: string }} Message
 */

/**
 * Create a toast component
 * @param {{messages: Message[]}} param0 initial messages
 * @returns
 */
function toastComponent({ messages }) {
  return {
    toastOptions: {
      delay: 3000,
    },

    handleMessages(event) {
      event.detail.messages.forEach((message) => this.createToast(message));
    },

    /**
     * Create a toast element
     * @param {Message} message
     */
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
      this.$nextTick(() => messages.forEach((message) => this.createToast(message)));
    },
  };
}
