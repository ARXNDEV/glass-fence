<template>
  <div class="connect">
    <div class="window">
      <div class="logo" title="About Glass Fence" @click.stop.prevent="about">
        <img src="/logo.svg" alt="Logo" class="logo-img" />
        <span class="brand-text">GLASS FENCE</span>
      </div>
      <form class="message" v-if="!connecting" @submit.stop.prevent="connect">
        <span v-if="!autoPassword">{{ $t('connect.login_title') }}</span>
        <span v-else>{{ $t('connect.invitation_title') }}</span>
        <input type="text" :placeholder="$t('connect.displayname')" v-model="displayname" autofocus />
        <input type="password" :placeholder="$t('connect.password')" v-model="password" v-if="!autoPassword" />
        <button type="submit" @click.stop.prevent="login">
          {{ $t('connect.connect') }}
        </button>
      </form>
      <div class="loader" v-if="connecting">
        <div class="bounce1"></div>
        <div class="bounce2"></div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .connect {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-primary);

    display: flex;
    justify-content: center;
    align-items: center;

    .window {
      width: 350px;
      background: var(--bg-card);
      border: 1px solid var(--border-default);
      border-radius: 0;
      padding: 40px 30px;

      .logo {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        color: $style-primary;
        margin-bottom: 20px;

        .logo-img {
          height: 32px;
          margin-bottom: 15px;
        }

        .brand-text {
          font-family: var(--font-display);
          font-size: 24px;
          font-weight: 700;
          letter-spacing: 2px;
          color: var(--text-primary);
        }
      }

      .message {
        display: flex;
        flex-direction: column;

        span {
          display: block;
          text-align: left;
          text-transform: uppercase;
          font-size: 10px;
          letter-spacing: 1px;
          color: var(--text-secondary);
          margin-bottom: 10px;
        }

        input {
          border: 1px solid var(--border-default);
          padding: 10px 12px;
          border-radius: 0;
          margin: 0 0 15px 0;
          background: var(--bg-primary);
          color: var(--text-primary);
          font-family: var(--text-mono);
          font-size: 12px;

          &::selection {
            background: rgba(255, 255, 255, 0.2);
          }
          &:focus {
            outline: none;
            border-color: var(--text-primary);
          }
        }

        button {
          cursor: pointer;
          border-radius: 0;
          padding: 10px;
          background: var(--text-primary);
          color: var(--bg-primary);
          text-transform: uppercase;
          font-weight: bold;
          font-family: var(--font-display);
          letter-spacing: 1px;
          margin: 10px 0 0 0;
          border: none;
          transition: opacity var(--transition);
          
          &:hover {
            opacity: 0.8;
          }
        }
      }

      .loader {
        width: 90px;
        height: 90px;
        position: relative;
        margin: 0 auto;

        .bounce1,
        .bounce2 {
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background-color: $style-primary;
          opacity: 0.6;
          position: absolute;
          top: 0;
          left: 0;

          -webkit-animation: bounce 2s infinite ease-in-out;
          animation: bounce 2s infinite ease-in-out;
        }

        .bounce2 {
          -webkit-animation-delay: -1s;
          animation-delay: -1s;
        }
      }
    }

    @keyframes bounce {
      0%,
      100% {
        transform: scale(0);
        -webkit-transform: scale(0);
      }
      50% {
        transform: scale(1);
        -webkit-transform: scale(1);
      }
    }
  }
</style>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator'

  @Component({ name: 'neko-connect' })
  export default class extends Vue {
    private autoPassword: string | null = new URL(location.href).searchParams.get('pwd')

    private displayname: string = ''
    private password: string = ''

    mounted() {
      // auto-password fill
      let password = this.$accessor.password
      if (this.autoPassword !== null) {
        this.removeUrlParam('pwd')
        password = this.autoPassword
      }

      // auto-user fill
      let displayname = this.$accessor.displayname
      const usr = new URL(location.href).searchParams.get('usr')
      if (usr) {
        this.removeUrlParam('usr')
        displayname = this.$accessor.displayname || usr
      }

      if (displayname !== '' && password !== '') {
        this.$accessor.login({ displayname, password })
        this.autoPassword = null
      }
    }

    get connecting() {
      return this.$accessor.connecting
    }

    removeUrlParam(param: string) {
      let url = document.location.href
      let urlparts = url.split('?')

      if (urlparts.length >= 2) {
        let urlBase = urlparts.shift()
        let queryString = urlparts.join('?')

        let prefix = encodeURIComponent(param) + '='
        let pars = queryString.split(/[&;]/g)
        for (let i = pars.length; i-- > 0; ) {
          if (pars[i].lastIndexOf(prefix, 0) !== -1) {
            pars.splice(i, 1)
          }
        }

        url = urlBase + (pars.length > 0 ? '?' + pars.join('&') : '')
        window.history.pushState('', document.title, url)
      }
    }

    login() {
      let password = this.password
      if (this.autoPassword !== null) {
        password = this.autoPassword
      }

      if (this.displayname == '') {
        this.$swal({
          title: this.$t('connect.error') as string,
          text: this.$t('connect.empty_displayname') as string,
          icon: 'error',
        })
        return
      }

      this.$accessor.login({ displayname: this.displayname, password })
      this.autoPassword = null
    }

    about() {
      this.$accessor.client.toggleAbout()
    }
  }
</script>
