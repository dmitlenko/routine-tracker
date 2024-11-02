/**
 * @param {{ chartUrl: string, chartId: string }}
 */
function dateRangeComponent({chartUrl, chartId}) {
  return {
    /**
     * @type {Element}
     */
    fromEl: null,
    /**
     * @type {Element}
     */
    toEl: null,
    /**
     * @type {string}
     */
    chartId: chartId,
    /**
     * @type {string}
     */
    chartUrl: chartUrl,
    /**
     * @param {string} from
     * @param {string} to
     */
    updateUrl(from, to){
      const url = new URL(window.location.href);
      url.searchParams.set("from", from);
      url.searchParams.set("to", to);
      window.history.pushState({}, "", url);
    },
    createSearchParams(from, to) {
      const params = new URLSearchParams();
      params.set("from", from);
      params.set("to", to);
      return params;
    },
    onChange() {
      const [from, to] = [this.fromEl.value, this.toEl.value];

      if (from && to) {
        this.updateUrl(from, to);
        const params = this.createSearchParams(from, to);

        htmx.ajax('GET', `${this.chartUrl}?${params.toString()}`, {
          target: `#${this.chartId}`,
          swap: 'outerHTML',
        });
      }
    },
    bind() {
      return {
        "@change": this.onChange,
        "@hx-chart-update.window": this.onChange,
      };
    },
    init() {
      this.$nextTick(() => {
        this.fromEl = this.$refs.from;
        this.toEl = this.$refs.to;
      });
    },
  };
}
