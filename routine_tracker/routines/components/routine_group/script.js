function routineGroupComponent() {
  return {
    /**
     * Update the color of the icon of a routine group
     * @param {Element} strip
     * @returns
     */
    updateIconColor(strip) {
      // Get icon element
      const icon = strip.querySelector("i");

      // Only update the color if the icon exists
      if (!icon) return;

      // Get the recommended text color
      const color = getRecomendedTextColor({ element: strip });

      // Update the icon color
      icon.style.color = color;
    },
    /**
     * Initialize the routine group component
     */
    init() {
      // Get the group element
      this.group = this.$el;

      // Update the icon color
      this.updateIconColor(this.group.querySelector("#colorStrip"));
    },
  };
}
