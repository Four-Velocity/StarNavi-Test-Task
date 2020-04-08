<template>
  <main>
    <aside>
      <img id=logo src="@/assets/logo.png" alt="">
      <div class="form">
        <router-link :to="`/user/${id}`">
          <button class="big-button">
            Profile
          </button>
        </router-link>
        <button class="big-button" @click="openCreation">
          Create Post
        </button>
      </div>
      <div class="log-out">
        <button class="big-button" @click="logOut">
          Log Out
        </button>
      </div>
    </aside>
    <section>
      <article v-for="post in posts" :key="post" v-bind:id="post.id">
        <div class="header">
          {{post.title}}
        </div>
        <div class="content">
          <img v-if="post.image" v-bind:src="post.image" alt="none">
          <div class="text">
            {{post.text}}
          </div>
        </div>
        <div class="footer">
          <div class="left">
            <button class="like-button" @click="like(post)">
              <img v-if="post.likes_list.includes(id)" src="@/assets/like.svg">
              <img v-else src="@/assets/unlike.svg">
              {{post.likes}}
            </button>
          </div>
          <div class="center">
            <router-link class=button-a :to="`/user/${post.creator.id}`">
            <img v-bind:src="`http://127.0.0.1:8000${post.creator.avatar}`" class="creds-avatar">
              Created by:<br>{{post.creator.username}}
            </router-link>
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
                 @change="imageUploaded"
                 ref="fileInput"/>
          <label for="file-input" id="file-label">Upload Image</label>
          <p style="font-size: 3em; color: #f96900" v-bind:style="{opacity: fileUploaded}">
            &#x2713;
          </p>
        </div>
        <button class="big-button" @click="createPost">Create</button>
      </div>
      <button id="cross"
              @click="closeCreation"
              v-bind:style="{display: creationVision}">
        &#x2715;
      </button>
    </div>
  </main>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      id: parseInt(this.$cookies.get('id'), 10),
      retry: 0,
      posts: null,
      next_page: '',
      buttonText: 'Next Page',
      buttonDisable: false,
      creationWidth: '0',
      creationVision: 'none',
      fileUploaded: 0,
      creation: {
        title: null,
        text: null,
        image: null,
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
    loadPosts() {
      let url = 'http://127.0.0.1:8000/api/posts/all/';
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
            this.loadPosts();
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
    imageUploaded(event) {
      // eslint-disable-next-line prefer-destructuring
      this.creation.image = event.target.files[0];
      this.fileUploaded = '100%';
    },
    createPost() {
      const url = 'http://127.0.0.1:8000/api/posts/all/';
      const formData = new FormData();
      formData.append('title', this.creation.title);
      formData.append('text', this.creation.text);
      formData.append('image', this.creation.image, this.creation.image.name);
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
        .then(() => this.closeCreation())
        .catch();
    },
    closeCreation() {
      const input = this.$refs.fileInput;
      input.type = 'text';
      input.type = 'image';
      this.fileUploaded = '0';
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
    logOut() {
      this.$cookies.remove('access');
      this.$cookies.remove('refresh');
      this.$cookies.remove('id');
      this.$router.push('/login/');
    },
  },
  mounted() {
    this.loadPosts();
  },
};
</script>
