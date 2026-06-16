import { getterTree, mutationTree, actionTree } from 'typed-vuex'
import { get, set } from '~/utils/localstorage'

export const namespaced = true

export const state = () => ({
  side: get<boolean>('side', false),
  tab: get<string>('tab', 'chat'),
  about: false,
  about_page: '',
  // AI Threat State
  threatLevel: 'OFFLINE' as 'OFFLINE' | 'CLEAR' | 'CAUTION' | 'CRITICAL',
  threatScore: 0 as number,
  currentURL: '' as string,
  aiConnected: false as boolean,
  threatsBlocked: 0 as number,
  lastThreatReasons: [] as string[],
})

export const getters = getterTree(state, {
  isThreatActive: (state) => state.threatLevel === 'CAUTION' || state.threatLevel === 'CRITICAL',
})

export const mutations = mutationTree(state, {
  setTab(state, tab: string) {
    state.tab = tab
    set('tab', tab)
  },
  setAbout(state, page: string) {
    state.about_page = page
  },
  toggleAbout(state) {
    state.about = !state.about
  },
  toggleSide(state) {
    state.side = !state.side
    set('side', state.side)
  },
  setSide(state, side: boolean) {
    state.side = side
    set('side', side)
  },
  // AI mutations
  setThreatLevel(state, level: 'OFFLINE' | 'CLEAR' | 'CAUTION' | 'CRITICAL') {
    state.threatLevel = level
  },
  setThreatScore(state, score: number) {
    state.threatScore = score
  },
  setCurrentURL(state, url: string) {
    state.currentURL = url
  },
  setAIConnected(state, connected: boolean) {
    state.aiConnected = connected
    if (connected && state.threatLevel === 'OFFLINE') {
      state.threatLevel = 'CLEAR'
    }
    if (!connected) {
      state.threatLevel = 'OFFLINE'
    }
  },
  incrementThreatsBlocked(state) {
    state.threatsBlocked++
  },
  setThreatsBlocked(state, count: number) {
    state.threatsBlocked = count
  },
  setLastThreatReasons(state, reasons: string[]) {
    state.lastThreatReasons = reasons
  },
})

export const actions = actionTree({ state, getters, mutations }, {})
