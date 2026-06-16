import { accessor as glassfence } from './store'
import { PluginObject } from 'vue'

// Plugins
import Logger from './plugins/log'
import Client from './plugins/glassfence'
import Axios from './plugins/axios'
import Swal from './plugins/swal'
import Anime from './plugins/anime'
import { i18n } from './plugins/i18n'

// Components
import Connect from '~/components/connect.vue'
import Video from '~/components/video.vue'
import Menu from '~/components/menu.vue'
import Side from '~/components/side.vue'
import Controls from '~/components/controls.vue'
import Members from '~/components/members.vue'
import Emotes from '~/components/emotes.vue'
import About from '~/components/about.vue'
import Header from '~/components/header.vue'
import Chat from '~/components/chat.vue'
import Clipboard from '~/components/clipboard.vue'
import Emoji from '~/components/emoji.vue'
import Emote from '~/components/emote.vue'
import Context from '~/components/context.vue'
import Markdown from '~/components/markdown'
import Avatar from '~/components/avatar.vue'

// Vue
import Vue from 'vue'
import ToolTip from 'v-tooltip'

Vue.use(ToolTip)

const exportMixin = {
  computed: {
    $accessor() {
      return glassfence
    },
    $client() {
      return window.$client
    },
  },
}

const plugini18n: PluginObject<undefined> = {
  install(Vue) {
    Vue.prototype.i18n = i18n
    Vue.prototype.$t = i18n.t.bind(i18n)
    Vue.prototype.$te = i18n.te.bind(i18n)
  },
}

function extend(component: any) {
  return component.use(plugini18n).use(Logger).use(Axios).use(Swal).use(Anime).use(Client).extend(exportMixin)
}

export const GlassFenceConnect = extend(Connect)
export const GlassFenceVideo = extend(Video)
export const GlassFenceMenu = extend(Menu)
export const GlassFenceSide = extend(Side)
export const GlassFenceControls = extend(Controls)
export const GlassFenceMembers = extend(Members)
export const GlassFenceEmotes = extend(Emotes)
export const GlassFenceAbout = extend(About)
export const GlassFenceHeader = extend(Header)
export const GlassFenceChat = extend(Chat)
export const GlassFenceClipboard = extend(Clipboard)
export const GlassFenceEmoji = extend(Emoji)
export const GlassFenceEmote = extend(Emote)
export const GlassFenceMarkdown = extend(Markdown)
export const GlassFenceContext = extend(Context)
export const GlassFenceAvatar = extend(Avatar)

glassfence.initialise()
export default glassfence
