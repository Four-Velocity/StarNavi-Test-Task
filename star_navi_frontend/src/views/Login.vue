<template>
  <aside>
    <img id=logo src="@/assets/logo.png" alt="">
    <div class="form">
      <div class="errmsg"
           v-bind:class="{danger: isDanger}">{{ msg }}</div>
      <input class="char-input" type="text" v-model="username" placeholder="Username"/>
      <input class="char-input" type="password" v-model="password" placeholder="Password">
      <button class="big-button" @click="login">Sign In</button>
      <p>
        Don't have an account yet?<br>
        <router-link class="button-a" to="/register">Sign Up</router-link>
      </p>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      msg: '',
      isDanger: false,
    };
  },
  methods: {
    getId() {
      this.$http.get('http://127.0.0.1:8000/auth/users/me/', { headers: { Authorization: `Bearer ${this.$cookies.get('access')}` } })
        .then((response) => {
          this.$cookies.set('id', response.data.id, '1d');
          this.$router.push('/');
        })
        .catch(() => {
          this.isDanger = true;
          this.msg = 'Hey, smth goes wrong, pls try again!';
        });
    },
    login() {
      const data = this.$qs.stringify({ username: this.username, password: this.password });
      const config = {
        headers: {
          'Content-type': 'application/x-www-form-urlencoded',
        },
      };
      this.$http.post('http://127.0.0.1:8000/auth/jwt/create/', data, config)
        .then((response) => {
          this.$cookies.set('access', response.data.access, '5MIN');
          this.$cookies.set('refresh', response.data.refresh, '1d');
          this.getId();
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.isDanger = false;
            this.msg = 'Incorrect email or password!';
          } else {
            this.isDanger = true;
            this.msg = 'Hey, smth goes wrong, pls try again!';
          }
        });
    },
  },
};
</script>
