class MaintainXCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.innerHTML = `
        <ha-card style="background: rgba(30, 16, 66, 0.5); backdrop-filter: blur(16px); border-radius: 24px; color: white; padding: 16px;">
          <div class="card-content">
            <h2>MaintainX Portal</h2>
            <p>Click below to log a direct work order.</p>
          </div>
        </ha-card>
      `;
      this.content = true;
    }
  }

  setConfig(config) {
    this.config = config;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('maintainx-card', MaintainXCard);
