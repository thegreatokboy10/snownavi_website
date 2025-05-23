/**
 * SnowNavi Navigation Module
 * This module handles loading and rendering the navigation bar based on the configuration from the server.
 */

class NavigationManager {
  constructor() {
    this.navConfig = null;
    this.currentLang = 'en';
    this.navContainer = null;
  }

  /**
   * Initialize the navigation manager
   * @param {string} navContainerId - The ID of the navigation container element
   * @param {string} langSelectId - The ID of the language selector element
   */
  async init(navContainerId = 'nav-links', langSelectId = 'lang') {
    this.navContainer = document.getElementById(navContainerId);

    if (!this.navContainer) {
      console.error('Navigation container not found:', navContainerId);
      return;
    }

    // Get the current language - prioritize localStorage over langSelect.value
    // This ensures we use the user's preference even before the language selector is set
    this.currentLang = localStorage.getItem('preferredLang') ||
                      (navigator.language.startsWith('zh') ? 'zh' :
                       navigator.language.startsWith('nl') ? 'nl' : 'en');

    const langSelect = document.getElementById(langSelectId);
    if (langSelect) {
      // Set the language selector to match our determined language
      langSelect.value = this.currentLang;

      // Listen for language changes
      langSelect.addEventListener('change', (e) => {
        this.currentLang = e.target.value;
        this.renderNavigation();
      });
    }

    try {
      // Load navigation configuration
      await this.loadNavConfig();

      // Render the navigation
      this.renderNavigation();
    } catch (error) {
      console.error('Error initializing navigation:', error);
    }
  }

  /**
   * Load the navigation configuration from the server
   */
  async loadNavConfig() {
    try {
      const response = await fetch('/data/navigation.json');
      if (!response.ok) {
        throw new Error(`Failed to load navigation config: ${response.status} ${response.statusText}`);
      }
      this.navConfig = await response.json();
      return this.navConfig;
    } catch (error) {
      console.error('Error loading navigation config:', error);
      // Fallback to default navigation if loading fails
      this.navConfig = this.getDefaultNavConfig();
      return this.navConfig;
    }
  }

  /**
   * Get default navigation configuration as a fallback
   */
  getDefaultNavConfig() {
    return {
      items: [
        {
          id: 'courses',
          url: 'index.html#courses',
          translations: {
            en: 'Courses',
            zh: '课程',
            nl: 'Cursussen'
          },
          visible: true,
          order: 1
        },
        {
          id: 'map',
          url: 'index.html#map',
          translations: {
            en: 'Interactive Ski Map',
            zh: '在线滑雪地图',
            nl: 'Interactieve Skikaart'
          },
          visible: true,
          order: 2
        },
        {
          id: 'story',
          url: 'index.html#story',
          translations: {
            en: 'Our Story',
            zh: '我们的故事',
            nl: 'Ons Verhaal'
          },
          visible: true,
          order: 3
        },
        {
          id: 'contact',
          url: 'index.html#contact',
          translations: {
            en: 'Contact',
            zh: '联系我们',
            nl: 'Contact'
          },
          visible: true,
          order: 4
        }
      ]
    };
  }

  /**
   * Render the navigation based on the current configuration and language
   */
  renderNavigation() {
    if (!this.navContainer || !this.navConfig) return;

    // Clear existing navigation items (except language selector)
    const langSelector = this.navContainer.querySelector('.language-selector');
    this.navContainer.innerHTML = '';

    if (langSelector) {
      this.navContainer.appendChild(langSelector);
    }

    // Sort navigation items by order
    const sortedItems = [...this.navConfig.items]
      .filter(item => item.visible)
      .sort((a, b) => a.order - b.order);

    // Create and append navigation items
    sortedItems.forEach(item => {
      // Skip items with null URL (hidden from navigation)
      if (item.url === null) return;

      const navItem = document.createElement('a');
      navItem.href = item.url;
      navItem.id = `nav-${item.id}`;
      navItem.textContent = item.translations[this.currentLang] || item.translations.en;

      // Insert before the language selector
      if (langSelector) {
        this.navContainer.insertBefore(navItem, langSelector);
      } else {
        this.navContainer.appendChild(navItem);
      }
    });
  }
}

// Create a global instance of the navigation manager
const navigationManager = new NavigationManager();

// Initialize the navigation as soon as possible
// Use an immediately-invoked function expression to initialize
(async function() {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    await new Promise(resolve => {
      document.addEventListener('DOMContentLoaded', resolve, { once: true });
    });
  }

  // Initialize navigation
  await navigationManager.init();

  // Make navigationManager available globally
  window.navigationManager = navigationManager;
})();
