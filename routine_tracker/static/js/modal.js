function modalComponent() {
  return {
    extraOptions: {},

    handleModal(event) {
      // Wait for next tick to ensure that the modal is rendered
      this.$nextTick(() => {
        // Get options from event
        const options = event.detail;

        // Create new modal instance
        const modal = new bootstrap.Modal(this.$el, {
          ...this.extraOptions,
          ...options,
        });

        // Show modal
        modal.show();
      });
    },
  };
}
