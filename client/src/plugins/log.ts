import { PluginObject } from 'vue'

interface Logger {
  error(error: Error): void
  warn(...log: any[]): void
  info(...log: any[]): void
  debug(...log: any[]): void
}

declare global {
  const $log: Logger

  interface Window {
    $log: Logger
  }
}

declare module 'vue/types/vue' {
  interface Vue {
    $log: Logger
  }
}

const plugin: PluginObject<undefined> = {
  install(Vue) {
    window.$log = {
      error: (error: Error) => console.error('[%cARXN%c] %cERR', 'color: #00d4ff;', '', 'color: #d84949;', error),
      warn: (...log: any[]) => console.warn('[%cARXN%c] %cWRN', 'color: #00d4ff;', '', 'color: #eae364;', ...log),
      info: (...log: any[]) => console.info('[%cARXN%c] %cINF', 'color: #00d4ff;', '', 'color: #4ac94c;', ...log),
      debug: (...log: any[]) => console.log('[%cARXN%c] %cDBG', 'color: #00d4ff;', '', 'color: #eae364;', ...log),
    }

    Vue.prototype.$log = window.$log
  },
}

export default plugin
