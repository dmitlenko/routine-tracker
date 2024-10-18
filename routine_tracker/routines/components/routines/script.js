/**
 * Navigation component for routines
 * @param {number} firstId
 * @returns
 */
function routinesNavigationComponent(firstId) {
  return {
    /**
     * Check if the navigation id is active
     * @param {number | string} id
     * @returns {boolean}
     */
    isActive(id) {
      return this.navId === id;
    },
    /**
     * Get the active class for the navigation
     * @param {number | string} id
     * @returns {string}
     */
    getActiveClass(id) {
      return this.isActive(id) ? "active" : "";
    },
    /**
     * Get the aria-current value for the navigation
     * @param {number | string} id
     * @returns {string}
     */
    ariaCurrent(id) {
      return this.isActive(id) ? "true" : "false";
    },
    /**
     * Set the active navigation id
     * @param {number | string} id
     */
    setActive(id) {
      this.navId = id;
    },
    /**
     * Initialize the navigation component
     */
    init() {
      this.navId = firstId;
    },
  };
}
