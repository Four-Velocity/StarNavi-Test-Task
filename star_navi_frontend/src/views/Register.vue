<template>
  <main>
    <aside>
      <img id=logo src="@/assets/logo.png" alt="">
      <div class="form">
        <div class="errmsg"
             :class="{danger: isDanger}"
             :style="{visibility: visible.error}">
          {{msg}}
        </div>
        <p>
          <a class="button-a" @click="step1Continue" :style="{visibility: visible.continue}">
            Continue anyway
          </a>
        </p>
        <input class="char-input"
               type="email"
               v-model="register.email"
               :disabled="steps.step1"
               placeholder="Email">
        <input class="char-input"
               type="text"
               v-model="register.username"
               :disabled="steps.step1"
               placeholder="UserName"/>
        <input class="char-input"
               type="password"
               v-model="register.password"
               :disabled="steps.step1"
               placeholder="Password"/>
        <input class="char-input"
               type="password"
               v-model="register.conf_password"
               :disabled="steps.step1"
               placeholder="Confirm Password"/>
        <input class="char-input"
               type="text"
               v-model="register.first_name"
               :disabled="steps.step1"
               placeholder="First Name"/>
        <input class="char-input"
               type="text"
               v-model="register.last_name"
               :disabled="steps.step1"
               placeholder="Last Name"/>
        <button class="big-button" v-bind:disabled="steps.step1" @click="step1">Continue</button>
        <p>
          Already have an account?<br>
          <a class="button-a" href="#/login/">Sign In</a>
        </p>
      </div>
    </aside>
    <section v-bind:style="{width: mainWidth}">
      <div class="register"   :style="{visibility: visible.step2}">
        <div id="avatar">
          <input type="file"
                 name="avatar"
                 id="avatar-input"
                 @change="avatarUploaded"
                 :disabled="steps.step2"
                 class="file-input"/>
          <label for="avatar-input" class="file-label">
            <img :src="uploadedAvatar" alt="avatar" class="uploaded">
            <div class="upload">
              <img src="@/assets/icons/photo.svg" alt="Upload Image">
            </div>
          </label>
        </div>
        <div>
          <label for="company">Company: </label>
          <input id="company"
                 class="char-input"
                 type="text"
                 maxlength="80"
                 :disabled="steps.step2"
                 v-model="additional.company"/>
        </div>
        <div>
          <label for="role">Role: </label>
          <input id="role"
                 class="char-input"
                 type="text"
                 maxlength="80"
                 :disabled="steps.step2"
                 v-model="additional.role"/>
        </div>
        <div>
          <label for="city">City: </label>
          <input id="city"
                 class="char-input"
                 type="text"
                 maxlength="50"
                 :disabled="steps.step2"
                 v-model="additional.city"/>
        </div>
        <div>
          <label for="country">Country: </label>
          <input id="country"
                 class="char-input"
                 type="text"
                 maxlength="50"
                 :disabled="steps.step2"
                 v-model="additional.country"/>
        </div>
        <div style="width: 100%">
          <label for="bio">Bio</label>
          <textarea id="bio"
                    rows="7" cols="28"
                    placeholder="Bio: Max 2048"
                    class="text-input"
                    type="text"
                    maxlength="2048"
                    :disabled="steps.step2"
                    v-model="additional.bio"/>
        </div>
        <button class="big-button" @click="step2">Finish Registration</button>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      register: {
        username: '',
        password: '',
        conf_password: '',
        first_name: '',
        last_name: '',
        email: '',
      },
      additional: {
        company: '',
        role: '',
        city: '',
        country: '',
        bio: '',
        avatar: '',
      },
      profileId: '',
      uploadedAvatar: '',
      changedAvatar: false,
      steps: {
        step1: false,
        step2: true,
      },
      msg: '',
      visible: {
        step2: 'hidden',
        error: 'hidden',
        continue: 'hidden',
      },
      isDanger: false,
      mainWidth: 0,
    };
  },
  methods: {
    step1() {
      this.visible.continue = 'hidden';
      this.visible.error = 'hidden';
      this.isDanger = false;
      if (this.register.password !== this.register.conf_password) {
        this.msg = 'Passwords are mismatch';
        this.visible.error = 'visible';
      } else {
        let data = {
          email: this.register.email,
        };
        data = this.$qs.stringify(data);
        const url = 'http://127.0.0.1:8000/auth/validate/';
        const config = {
          headers: {
            'Content-type': 'application/x-www-form-urlencoded',
          },
        };
        this.$http.post(url, data, config)
          .then((response) => {
            console.log(response.data.valid === 'risky');
            if (response.data.valid === 'undeliverable') {
              this.msg = 'Your email was marked as undeliverable! Provide another one!';
              this.visible.error = 'visible';
              this.isDanger = true;
            } else if (response.data.valid === 'risky') {
              this.msg = 'Your email was marked as risky! Provide another one or';
              this.visible.error = 'visible';
              this.visible.continue = 'visible';
              this.additional = response.data;
            } else {
              this.additional = response.data;
              this.step1Continue();
            }
          })
          .catch(() => {
            this.msg = 'Smth wrong, Please tr again! ';
            this.visible.error = 'visible';
            this.isDanger = true;
          });
      }
    },
    step1Continue() {
      let data = this.$qs.stringify(this.register);
      let url = 'http://127.0.0.1:8000/auth/users/';
      let config = {
        headers: {
          'Content-type': 'application/x-www-form-urlencoded',
        },
      };
      this.$http.post(url, data, config)
        .then((response1) => {
          this.$cookies.set('id', response1.data.id);
          data = this.$qs.stringify({
            username: this.register.username,
            password: this.register.password,
          });
          url = 'http://127.0.0.1:8000/auth/jwt/create/';
          this.$http.post(url, data, config)
            .then((response2) => {
              this.$cookies.set('access', response2.data.access, '5MIN');
              this.$cookies.set('refresh', response2.data.refresh, '1d');
              url = `http://127.0.0.1:8000/api/users/${response1.data.id}/`;
              config = {
                headers: {
                  Authorization: `Bearer ${response2.data.access}`,
                },
              };
              this.$http.get(url, config)
                .then((response3) => {
                  this.profileId = response3.data.results[0].profile.id;
                  this.mainWidth = '73vw';
                  this.visible.step2 = 'visible';
                  this.steps.step1 = true;
                  this.steps.step2 = false;
                  this.uploadedAvatar = `https://api.adorable.io/avatars/150/${this.register.username}.png`;
                })
                .catch(() => {
                  this.msg = 'Smth wrong, Please tr again! ';
                  this.visible.error = 'visible';
                  this.isDanger = true;
                });
            })
            .catch(() => {
              this.msg = 'Smth wrong, Please tr again! ';
              this.visible.error = 'visible';
              this.isDanger = true;
            });
        })
        .catch(() => {
          this.msg = 'Smth wrong, Please tr again! ';
          this.visible.error = 'visible';
          this.isDanger = true;
        });
    },
    step2() {
      const url = `http://127.0.0.1:8000/api/profile/${this.profileId}/`;
      const config = {
        headers: {
          Authorization: `Bearer ${this.$cookies.get('access')}`,
        },
      };
      const formData = new FormData();
      formData.append('company', this.additional.company !== null ? this.additional.company : '');
      formData.append('role', this.additional.role !== null ? this.additional.role : '');
      formData.append('city', this.additional.city !== null ? this.additional.city : '');
      formData.append('country', this.additional.country !== null ? this.additional.country : '');
      formData.append('bio', this.additional.bio !== null ? this.additional.bio : '');
      if (this.changedAvatar) {
        formData.append('avatar', this.additional.avatar, this.additional.avatar.name);
      }
      this.$http.patch(url, formData, config)
        .then(() => this.$router.push('/'))
        .catch(() => {
          this.msg = 'Smth wrong, Please tr again! ';
          this.visible.error = 'visible';
          this.isDanger = true;
        });
    },
    avatarUploaded(event) {
      // eslint-disable-next-line prefer-destructuring
      this.additional.avatar = event.target.files[0];
      this.uploadedAvatar = URL.createObjectURL(this.additional.avatar);
      this.changedAvatar = true;
    },
  },
};
</script>

<style scoped>

</style>
