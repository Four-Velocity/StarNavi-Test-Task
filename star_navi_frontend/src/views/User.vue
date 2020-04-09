<template>
  <main>
    <aside>
      <router-link to="/">
        <img id=logo src="@/assets/logo.png" alt="">
      </router-link>
      <div class="profile">
        <div id="avatar">
          <input type="file"
                 name="avatar"
                 id="avatar-input"
                 @change="avatarUploaded"
                 :disabled="editing.disabled"
                 class="file-input"/>
          <label for="avatar-input" class="file-label">
            <img :src="uploadedAvatar" alt="avatar" class="uploaded">
            <div class="upload"  :style="{visibility: editing.visible}">
              <img src="@/assets/icons/photo.svg" alt="Upload Image">
            </div>
          </label>
        </div>
        <nav v-if="owner">
          <button @click="allowEdit">
            <img src="@/assets/icons/pencil.png" alt="Edit profile">
            <span class="tooltip">Edit profile</span>
          </button>
          <button @click="openCreation">
            <img src="@/assets/icons/add.png" alt="Create Post">
            <span class="tooltip">Create Post</span>
          </button>
          <button @click="logOut">
            <img src="@/assets/icons/logout.png" alt="Log Out">
            <span class="tooltip">Log Out</span>
          </button>
        </nav>
        <div class="info">
          <div style="width: 100%">
          <textarea id="bio"
                    rows="7" cols="28"
                    class="info-input"
                    type="text"
                    :disabled="editing.disabled"
                    v-model="profile.profile.bio"/>
          </div>
          <div style="width: 100%">
          <label for="username">Username: </label>
          <input id="username"
                 class="info-input"
                 type="text"
                 disabled="disabled"
                 v-model="profile.profile.username"/>
          </div>
          <div style="width: 100%">
          <label for="email">Email: </label>
          <input id="email"
                 class="info-input"
                 type="email"
                 disabled="disabled"
                 v-model="profile.profile.email"/>
          </div>
          <div style="width: 100%">
          <label for="full-name">Full name: </label>
          <input id="full-name"
                 class="info-input"
                 type="text"
                 disabled="disabled"
                 v-model="profile.profile.full_name"/>
          </div>
          <div style="width: 100%">
          <label for="company">Company: </label>
          <input id="company"
                 class="info-input"
                 type="text"
                 :disabled="editing.disabled"
                 v-model="profile.profile.company"/>
          </div>
          <div style="width: 100%">
          <label for="role">Role: </label>
          <input id="role"
                 class="info-input"
                 type="text"
                 :disabled="editing.disabled"
                 v-model="profile.profile.role"/>
          </div>
          <div style="width: 100%">
          <label for="city">City: </label>
          <input id="city"
                 class="info-input"
                 type="text"
                 :disabled="editing.disabled"
                 v-model="profile.profile.city"/>
          </div>
          <div style="width: 100%">
          <label for="country">Country: </label>
          <input id="country"
                 class="info-input"
                 type="text"
                 :disabled="editing.disabled"
                 v-model="profile.profile.country"/>
          </div>

          <div id="finish">
            <button style="color: lightcoral"
                    @click="stopEdit"
                    :style="{visibility: editing.visible}">
              &#x2715;
            </button>
            <button style="color: lightgreen"
                    @click="updateProfile"
                    :style="{visibility: editing.visible}">
              &#x2713;
            </button>
          </div>
        </div>
      </div>
    </aside>
    <section>
      <article v-for="post in posts" :key="post" v-bind:id="post.id">
        <div class="header">
          <p>
            {{post.title}}
          </p>
          <img class="trash"
               v-if="owner"
               @click="deletePost(post)"
               src="@/assets/icons/trash.svg"
          alt="&#x2715;">
        </div>
        <div class="content">
          <img v-if="post.image" v-bind:src="post.image" alt="none">
          <div v-if="post.text" class="text">
            {{post.text}}
          </div>
        </div>
        <div class="footer" style="padding-left: 25%">
          <div class="left">
            <button class="like-button" @click="like(post)">
              <img v-if="post.likes_list.includes(id)" src="@/assets/icons/like.svg">
              <img v-else src="@/assets/icons/unlike.svg">
              {{post.likes}}
            </button>
          </div>
          <div class="right">
            {{post.pub_date | moment("MM Do YYYY, dd") }} <br>
            {{post.pub_date | moment("HH:mm")}}
          </div>
        </div>
      </article>
      <footer>
        <button class="big-button" @click="loadPosts"
                v-bind:disabled="buttonDisable">{{ buttonText }}</button>
      </footer>
    </section>
    <div id="post-bg" v-bind:style="{width: creationWidth}">
      <div id="post-form" v-bind:style="{display: creationVision}">
        <input class="char-input"
               maxlength="200"
               placeholder="Title"
               v-model="creation.title"/>
        <textarea class="text-input"
                  placeholder="Text"
                  v-model="creation.text"
                  cols="80" rows="20"/>
        <div style="text-align: center">
          <input type="file"
                 name="file"
                 id="file-input"
                 class="file-input"
                 @change="imageUploaded"
                 ref="fileInput"/>
          <label for="file-input" class="file-label">
            <div class="image-upload">
              <img :src="uploadedImage" class="uploaded">
              <div  class="upload">
                <img src="@/assets/icons/photo.svg" alt="Upload Image">
              </div>
            </div>
          </label>
        </div>
        <button class="big-button" @click="createPost">Create</button>
      </div>
      <button class="cross"
              @click="closeCreation"
              v-bind:style="{display: creationVision}">
        &#x2715;
      </button>
    </div>
  </main>
</template>

<script>
export default {
  name: 'User',
  data() {
    return {
      id: parseInt(this.$cookies.get('id'), 10),
      retry: 0,
      posts: null,
      next_page: '',
      buttonText: 'Next Page',
      buttonDisable: false,
      owner: false,
      creationWidth: '0',
      creationVision: 'none',
      uploadedImage: null,
      uploadedAvatar: null,
      avatarChanged: false,
      creation: {
        title: null,
        text: null,
        image: null,
      },
      profile: null,
      editing: {
        disabled: true,
        visible: 'hidden',
      },
    };
  },
  methods: {
    // eslint-disable-next-line consistent-return
    getToken() {
      const access = this.$cookies.get('access');
      const refresh = this.$cookies.get('refresh');
      if (access !== null) {
        return access;
      }
      if (refresh !== null) {
        const url = 'http://127.0.0.1:8000/auth/jwt/refresh/';
        const config = {
          headers: {
            'Content-type': 'application/x-www-form-urlencoded',
          },
        };
        // eslint-disable-next-line
        const data = this.$qs.stringify({ refresh: refresh });
        this.$http.post(url, data, config)
          .then((response) => {
            this.$cookies.set('access', response.data.access, '5MIN');
            return response.data.access;
          });
      }
      if (refresh === null) {
        this.$router.push('/login');
      }
    },
    loadPosts(username) {
      const userId = this.$route.params.id;
      this.owner = userId === this.$cookies.get('id');
      let url = `http://127.0.0.1:8000/api/posts/${username}/`;
      if (this.next_page !== '') {
        url = this.next_page;
      }
      if (this.next_page === null) {
        this.buttonText = 'That\'s all!';
        this.buttonDisable = true;
        this.$forceUpdate();
      }
      const token = this.getToken();
      this.$http.get(url, { headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          this.retry = 0;
          if (this.posts === null) {
            this.next_page = response.data.next;
            this.posts = response.data.results;
          } else {
            this.next_page = response.data.next;
            this.posts = this.posts.concat(response.data.results);
          }
        })
        .catch((error) => {
          if (error.response.status === 401 && this.retry < 4 && token === undefined) {
            this.retry += 1;
            this.loadPosts(username);
          }
        });
    },
    loadUser() {
      const userId = this.$route.params.id;
      this.owner = userId === this.$cookies.get('id');
      const url = `http://127.0.0.1:8000/api/users/${userId}/`;
      const token = this.getToken();
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      this.$http.get(url, config)
        .then((response) => {
          this.retry = 0;
          // eslint-disable-next-line prefer-destructuring
          this.profile = response.data.results[0];
          this.profile.profile.avatar = `http://127.0.0.1:8000${this.profile.profile.avatar}`;
          this.uploadedAvatar = this.profile.profile.avatar;
          this.$forceUpdate();
          this.loadPosts(this.profile.profile.username);
        })
        .catch((error) => {
          if (error.response.status === 401 && this.retry < 4 && token === undefined) {
            this.retry += 1;
            this.loadUser();
          }
        });
    },
    like(post) {
      const url = `http://127.0.0.1:8000/api/like/${post.id}/`;
      const token = this.getToken();
      const config = { headers: { Authorization: `Bearer ${token}` } };
      this.$http.put(url, null, config)
        .then(() => {
          if (!post.likes_list.includes(this.id)) {
            post.likes_list.unshift(this.id);
            // eslint-disable-next-line no-param-reassign
            post.likes += 1;
          } else {
            const index = post.likes_list.indexOf(this.id);
            if (index > -1) {
              post.likes_list.splice(index, 1);
            }
            // eslint-disable-next-line no-param-reassign
            post.likes -= 1;
          }
        })
        .catch();
    },
    deletePost(post) {
      const url = `http://127.0.0.1:8000/api/posts/${post.id}/`;
      const token = this.getToken();
      const config = { headers: { Authorization: `Bearer ${token}` } };
      this.$http.delete(url, config)
        .then(() => this.$router.go())
        .catch(() => alert('Smth go wrong pls try again'));
    },
    imageUploaded(event) {
      // eslint-disable-next-line prefer-destructuring
      this.creation.image = event.target.files[0];
      this.uploadedImage = URL.createObjectURL(this.creation.image);
    },
    avatarUploaded(event) {
      // eslint-disable-next-line prefer-destructuring
      this.profile.profile.avatar = event.target.files[0];
      this.uploadedAvatar = URL.createObjectURL(this.profile.profile.avatar);
      this.avatarChanged = true;
    },
    createPost() {
      const url = 'http://127.0.0.1:8000/api/posts/all/';
      const formData = new FormData();
      formData.append('title', this.creation.title);
      if (this.creation.text !== null) {
        formData.append('text', this.creation.text);
      } else {
        formData.append('text', '');
      }
      if (this.creation.image !== null) {
        formData.append('image', this.creation.image, this.creation.image.name);
      }
      // let data = { title: this.creation.title, text: this.creation.text };
      // data = this.$qs.stringify(data);
      const token = this.getToken();
      const config = {
        headers: {
          // 'Content-type': 'application/x-www-form-urlencoded',
          Authorization: `Bearer ${token}`,
        },
      };
      this.$http.post(url, formData, config)
        .then(() => {
          this.retry = 0;
          this.closeCreation();
          this.$router.go();
        })
        .catch((error) => {
          if (error.response.status === 401 && this.retry < 4 && token === undefined) {
            this.retry += 1;
            this.createPost();
          }
        });
    },
    closeCreation() {
      const input = this.$refs.fileInput;
      input.type = 'text';
      input.type = 'image';
      this.uploadedImage = null;
      this.creationVision = 'none';
      this.creationWidth = 0;
      this.creation = {
        title: null,
        text: null,
        image: null,
      };
    },
    openCreation() {
      this.creationWidth = '100vw';
      this.creationVision = 'flex';
    },
    allowEdit() {
      this.editing.disabled = false;
      this.editing.visible = 'visible';
    },
    stopEdit() {
      this.$router.go();
    },
    updateProfile() {
      const url = `http://127.0.0.1:8000/api/profile/${this.profile.profile.id}/`;
      const token = this.getToken();
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      const formData = new FormData();
      formData.append('company', this.profile.profile.company);
      formData.append('role', this.profile.profile.role);
      formData.append('city', this.profile.profile.city);
      formData.append('country', this.profile.profile.country);
      formData.append('bio', this.profile.profile.bio);
      if (this.avatarChanged) {
        formData.append('avatar', this.profile.profile.avatar, this.profile.profile.avatar.name);
      }
      this.$http.patch(url, formData, config)
        .then(() => {
          this.retry = 0;
          this.$router.go();
        })
        .catch((error) => {
          if (error.response.status === 401 && this.retry < 4 && token === undefined) {
            this.retry += 1;
            this.updateProfile();
          }
        });
    },
    logOut() {
      this.$cookies.remove('access');
      this.$cookies.remove('refresh');
      this.$cookies.remove('id');
      this.$router.push('/login/');
    },
  },
  mounted() {
    this.loadUser();
  },
};
</script>

<style scoped>

</style>
