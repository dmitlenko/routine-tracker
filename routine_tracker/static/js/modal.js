function modalComponent() {
  return {
    extraOptions: {},

    handleModal(event) {
      this.$nextTick(() => {
        const { id, options } = event.detail;

        const parent = document.getElementById(id).parentElement;

        const modal = new bootstrap.Modal(parent, {
          ...this.extraOptions,
          ...options,
        });

        modal.show();
      });
    },
  };
}
