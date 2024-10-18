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

      // Get rgb color of the strip
      const rgbString = getComputedStyle(strip).backgroundColor;

      // Convert rgb string to array
      const rgb = rgbString
        .slice(4, -1)
        .split(",")
        .map((value) => parseInt(value));

      // Calculate the brightness of the color
      const brightness = Math.round(
        (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
      );

      // Set the color of the icon based on the brightness
      strip.style.color = brightness > 125 ? "black" : "white";
    },

    init() {
      // Get the group element
      const group = this.$el;

      // Update the icon color
      this.updateIconColor(group);
    },
  };
}
