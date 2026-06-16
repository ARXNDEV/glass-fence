import { PluginObject } from 'vue'
import { GlassFenceClient } from '~/glassfence'

declare global {
  const $client: GlassFenceClient

  interface Window {
    $client: GlassFenceClient
  }
}

declare module 'vue/types/vue' {
  interface Vue {
    $client: GlassFenceClient
  }
}

const plugin: PluginObject<undefined> = {
  install(Vue) {
    window.$client = new GlassFenceClient()
      .on('error', window.$log.error)
      .on('warn', window.$log.warn)
      .on('info', window.$log.info)
      .on('debug', window.$log.debug)

    Vue.prototype.$client = window.$client
  },
}

export default plugin
