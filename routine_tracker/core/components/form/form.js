/**
 * @typedef {{ field: string, errors: string[] }} Context
 */

function formComponent({ callSubmit = false }) {
  return {
    submitting: false,
    submit() {
      this.$nextTick(() => {
        this.submitting = true;

        if (callSubmit) this.$el.submit();
      });
    },
    init() {
      this.$el.addEventListener("submit", (e) => {
        e.preventDefault();
        this.submit();
      });
    },
    /**
     * Bind the field attributes
     * @param {Context} context
     * @returns
     */
    bindField(context) {
      const { field } = context;
      return {
        "x-bind:class": () =>
        this.hasError(context, field) ? "is-invalid" : "",
        "x-bind:disabled": () => this.submitting,
        "x-on:keyup": () => this.clearError(context),
        "x-on:change": () => this.clearError(context),
      };
    },
    /**
     * Check if the field has an error
     * @param {Context} context
     * @returns {boolean}
     */
    hasError({ errors }) {
      return errors.length > 0;
    },
    /**
     * Add an error to the field
     * @param {Context} context
     */
    clearError(context) {
      context.errors = [];
    },
    /**
     * Get the error text for the field
     * @param {Context} context
     * @returns {string}
     */
    getErrorText(context) {
      if (!context.errors) return "";

      return context.errors.join(" ");
    },
  };
}
