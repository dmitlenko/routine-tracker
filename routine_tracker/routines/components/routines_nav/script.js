/**
 * Navigation component for routines
 * @param {{ initialId: number | string, targetId: string, loaderId: string }} firstId
 * @returns
 */
function routinesNavigationComponent({ initialId, targetId, loaderId }) {
  return {
    navId: initialId,
    targetId,
    loaderId,
    links: [],
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
     * Generate the link attributes for the navigation
     * @param {{ pk: number | 'create', get: string, push: string }} params
     * @returns
     */
    linkAttributes({ pk, get, push }) {
      const hx = get && push ? { "hx-get": get, "hx-push-url": push } : {};

      return {
        href: "#",
        "aria-current": this.ariaCurrent(pk),
        "x-on:click": () => this.setActive(pk),
        "x-ref": `nav-${pk}`,
        "x-bind:class": () => this.getActiveClass(pk),
        "x-init": () => this.addLink({ pk, get, push }),
        "hx-target": `#${this.targetId}`,
        "hx-swap": "innerHTML",
        "hx-indicator": `#${this.loaderId}`,
        ...hx,
      };
    },
    addLink({ pk, get, push }) {
      this.links.push({ pk, get, push });
    },

    deleteRoutine(id) {
      const obj = this.$refs[`nav-${id}`];

      if (obj) {
        // Delete the routine
        obj.parentElement.remove();

        // Remove the routine from the links
        this.links = this.links.filter((link) => link.pk !== id);

        // Set the first routine as active
        let pk = this.links
          .filter((link) => link.pk !== id && link.pk !== "create")
          .at(0)?.pk;

        // if pk is undefined, set to create
        if (!pk) pk = "create";

        // Set the active routine
        this.setActive(pk);

        // Click the active
        this.$refs[`nav-${pk}`].click();
      }
    },
  };
}
