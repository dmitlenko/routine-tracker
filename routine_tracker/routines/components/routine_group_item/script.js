/**
 * Deletes a routine group from the DOM
 * @param {number} id
 */
function deleteRoutineGroup(id) {
  // Get the element with the data-group-id attribute equal to the id
  const el = document.querySelector(`[data-group-id="${id}"]`);

  // Just delete the element if it exists
  if (el) {
    // Add fade class to animate the deletion
    el.classList.add("fade");

    // Wait for the animation to finish
    setTimeout(() => {
      // Remove the element from the DOM
      el.remove();
    }, 150);
  }
}

function routineGroupItemComponent() {
  return {
    /**
     * Update the color of the icon of a routine group
     * @param {Element} group
     * @param {string} color
     */
    updateIconColor(group) {
      // Get color strip element
      const strip = group.querySelector("#colorStrip");

      // Get icon element
      const icon = strip.querySelector("i");

      // Only update the color if the icon exists
      if (!icon) return;

      // Get the recommended text color
      const color = getRecomendedTextColor({ element: strip });

      // Update the icon color
      icon.style.color = color;
    },

    init() {
      // Get the group element
      const group = this.$el;

      // Update the icon color
      this.updateIconColor(group);
    },
  };
}
