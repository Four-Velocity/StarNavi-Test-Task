<template>
  <div id="app">
    <router-view/>
    <div id="bg">
      <img src="./assets/bigLogo.svg" alt="">
    </div>
  </div>
</template>

<style lang="sass">
  $accent: #f96900
  $waring: #ddd33e
  $alert: #ff442e
  $light: #ffffff
  $dark: #000000
  $gray: #939393
  $glass: fade_out(#7e7e7e, 0.5)
  $dark-glass: fade_out($dark, 0.3)
  $field_width: 18.2291666667vw
  $field_height: 4.62962962963vh

  @import url('https://fonts.googleapis.com/css2?family=Rokkitt:wght@400;600&family=Rubik:wght@300;500;700&display=swap')
  /* Page Styles*/
  *
    font-family: 'Rubik', sans-serif

  body
    padding: 0
    margin: 0
    background-image: url("./assets/Background.jpg")

  #bg
    margin: 0
    position: absolute
    bottom: 5vh
    right: 5vw
    z-index: -100

  /* Scrollbar*/
  ::placeholder
    color: $gray
  ::-webkit-scrollbar
    width: 1%
    border-radius: 15px
    margin: 1% 0
  ::-webkit-scrollbar-track
    background: $dark-glass
    border-radius: 15px
    box-shadow: inset 0 0 10px $glass
  ::-webkit-scrollbar-thumb
    background: $accent
    border-radius: 15px

  /*Conten styles*/
  main
    display: flex
    justify-content: space-between
    margin: 0
    padding: 0
    height: 100vh
    width: 100vw
    overflow-x: hidden
    overflow-y: hidden

  /*Sidebar base styles*/
  aside
    width: 25vw
    height: 100vh
    background-color: $glass
    backdrop-filter: blur(5px)
    border-radius: 0 15px 15px 0

    #logo
      width: 5.20833333333vw
      margin: (25vw - 5.20833333333vw)/5 (25vw - 5.20833333333vw)/2
      margin-bottom: 0

    .form
      margin-top: 37.5% - 25%
      text-align: center

      .errmsg
        width: $field_width
        height: 1.4em
        margin-left: auto
        margin-right: auto
        text-align: center
        font-size: 1.4em
        color: $waring
        visibility: visible
        text-shadow: 0 0 0.3em $waring
      .danger
        color: $alert
        text-shadow: 0 0 0.3em $alert
      p
        color: $light
        font-size: 1.4em

    .log-out
      min-height: 25vh
      position: relative
      display: flex
      justify-content: center
      align-items: flex-end

  /*Content div base styles*/
  section
    width: 73vw
    height: 100vh
    background-color: $glass
    backdrop-filter: blur(5px)
    border-radius:  15px 0 0 15px
    padding: 0.5%
    overflow-y: scroll

    .register
      color: $light
      width: 40vw
      height: 90%
      font-size: 1.3em
      display: flex
      flex-direction: column
      align-items: center
      justify-content: space-evenly
      margin: 1% auto auto
      #avatar
        border-radius: 15px
        height: $field_width/2.5
        width: $field_width/2.5
        .file-input:disabled + label
          cursor: default
        .file-input + label
          border-radius: 15px
          height: $field_width/2.5
          width: $field_width/2.5
          position: relative
          text-align: center
          .uploaded
            height: $field_width/2.5
            width: $field_width/2.5
            border-radius: 15px
          .upload
            width: $field_width/2.5
            height: $field_width/2.5*0.25
            position: absolute
            bottom: 0
            z-index: 10
            display: flex
            align-content: center
            justify-content: center
            border-radius: 0 0 15px 15px
            background-color: $glass
            img
              transition: 0.7s
              &:hover
                transform: scale(1.1)
      textarea
        resize: none
        width: 100%
  /*router urls styles*/
  .button-a, .button-a:visited
    font-size: 1.4em
    color: $accent
    text-decoration: none
  .button-a:hover
    text-decoration: underline
    cursor: pointer
  .button-a:disabled
    cursor: not-allowed
    text-decoration: none
  /*button styles-/
  .big-button
    border: 2px solid $accent
    border-radius: 15px
    width: $field_width
    height: $field_height
    background-color: #0000
    color: $light
    font-size: 1.5em
    margin-top: $field_height/2
    transition: 0.3s
    &:hover
      cursor: pointer
      background-color: fade_out($accent, 0.5)
      transform: scale(1.05)
    &:focus
      outline: none
    &:disabled
      cursor: not-allowed
      &:hover
        cursor: not-allowed
        background-color: #0000

  /*Small input styles*/
  .char-input
    border: none
    border-bottom: 2px solid $light
    width: $field_width
    height: $field_height
    font-size: 1.4em
    color: $light
    background-color: #0000
    text-align: center
    border-radius: 15px 15px 0 0
    margin-top: $field_height/2
    &:focus
      background-color: $glass
      outline: none
    &:disabled
      cursor: not-allowed

  /*Big input styles*/
  .text-input
    border: none
    border-bottom: 2px solid $light
    border-left: 2px solid $light
    border-bottom-left-radius: 15px
    border-top-right-radius: 15px
    font-size: 1em
    color: $light
    background-color: #0000
    text-align: center
    margin-bottom: 2%
    &:focus
      background-color: $glass
      outline: none
    &:disabled
      cursor: not-allowed

  .file-input
    width: 0.1px
    height: 0.1px
    opacity: 0
    overflow: hidden
    position: absolute
    z-index: -1
    & + label
      color: $light
      font-size: 1.4em
      cursor: pointer
      width: $field_width
      height: $field_height*4
      display: inline-block
      .image-upload
        width: $field_width
        height: $field_height*4
        border-radius: 15px
        text-align: center
        position: relative
        background-color: $glass
        .uploaded
          max-height: $field_height*4
          max-width: $field_width
          margin: 0
          border-radius: 15px

        .upload
          width: 100%
          height: $field_height*0.7
          background-color: $glass
          position: absolute
          bottom: 0
          z-index: 10
          display: flex
          align-content: center
          justify-content: center
          border-radius: 0 0 15px 15px
          img
            transition: 0.7s
            &:hover
              transform: scale(1.1)

  article
    width: 100%
    border-radius: 15px
    margin-bottom: 1%

    .header
      background-color: $light
      border-radius: 15px 15px 0 0
      color: $accent
      font-family: Rokkit, serif
      font-size: 2em
      text-align: center
      font-weight: 700
      display: flex
      padding-left: 10%
      /*flex-direction: row*/
      /*align-content: center*/
      /*justify-content: space-around*/
      p
        font-family: Rokkit, serif
        font-size: 1.3em
        text-align: center
        font-weight: 700
        width: 90%
        align-self: center
        margin: 0
      .trash
        width: 1.7em
        height: 1.7em
        cursor: pointer
        transition: 0.7s
        &:hover
          transform: scale(1.1)


    .content
      margin-top: 0.5%
      width: 100%
      background-color: $light
      text-align: center
      img
        max-width: 50%
        max-height: 50vh
        margin: 1%
        box-shadow: 0 0 10px $dark-glass
        border-radius: 15px
        transition: transform .7s
        &:hover
          transform: scale(1.01)
      .text
        margin: 0.5% 15%
        padding: 1%
        font-family: Rokkit, serif
        font-size: 1.25em
        font-weight: 500
    .footer
      box-sizing: border-box
      width: 100%
      border-radius: 0 0 15px 15px
      border: solid 2px $accent
      background-color: $glass
      backdrop-filter: blur(5px)
      display: flex
      /*justify-content: space-around*/
      align-items: center

      div
        width: 33.3333333333%
        color: $light
        display: flex
        align-items: center
        justify-content: center

      .left
        button
          border: none
          background-color: #0000
          color: $light
          display: flex
          align-items: center
          font-size: 1.1em
          cursor: pointer
          margin: 0.5% 0
          transition: 0.7s
          &:hover
            transform: scale(1.1)
          &:focus
            outline: none

      .center
        .button-a
          font-size: 1.1em
          display: flex
          align-items: center
          color: $light
          margin: 0.5% 0
          transition: 0.7s
          &:hover
            transform: scale(1.025)

        .creds-avatar
          width: 3em
          border-radius: 15px

  footer
    .big-button
      margin-bottom: 2%
      width: 100%
      &:disabled
        cursor: default

  #post-bg
    position: absolute
    height: 100vh
    left: 0
    margin: 0
    background-color: $dark-glass
    backdrop-filter: blur(5px)
    z-index: 1
    transition: 0.5s
    transition-timing-function: ease-out


    .cross
      border: none
      background-color: #0000
      color: $accent
      font-size: 3em
      position: absolute
      top: 2vh
      right: 2vw
      cursor: pointer
      transition: 0.7s
      transition-timing-function: ease-in-out
      &:focus
        outline: none
      &:hover
        transform: scale(1.2)

    #post-form
      height: 100vh
      margin: auto
      display: flex
      flex-direction: column
      justify-content: space-around
      align-items: center

  .profile
    display: flex
    flex-direction: column
    align-items: center
    justify-content: space-around
    margin: 1% auto auto

    #avatar
      border-radius: 15px
      height: $field_width/2.5
      width: $field_width/2.5
      .file-input:disabled + label
          cursor: default
      .file-input + label
        border-radius: 15px
        height: $field_width/2.5
        width: $field_width/2.5
        position: relative
        text-align: center
        .uploaded
          height: $field_width/2.5
          width: $field_width/2.5
          border-radius: 15px
        .upload
          width: $field_width/2.5
          height: $field_width/2.5*0.25
          position: absolute
          bottom: 0
          z-index: 10
          display: flex
          align-content: center
          justify-content: center
          border-radius: 0 0 15px 15px
          background-color: $glass
          img
            transition: 0.7s
            &:hover
              transform: scale(1.1)
    nav
      margin: 2% 0
      height: $field_height/2
      width: $field_width
      display: flex
      align-content: center
      justify-content: space-around

      button
        height: $field_height
        background: none
        border: none
        cursor: pointer
        transition: 0.7s
        &:hover
          transform: scale(1.1)
        &:focus
          outline: none
        &:hover .tooltip
          visibility: visible
          opacity: 1
        .tooltip
          visibility: hidden
          opacity: 0
          width: $field_height*3
          background: $glass
          backdrop-filter: blur(5px)
          color: $light
          text-align: center
          padding: 5px 0
          border-radius: 15px

          position: absolute
          z-index: 1
          bottom: 125%
          left: -60%
          transition: 0.7s
          transition-timing-function: ease-in-out
        img
          height: $field_height
          width: $field_height
    .info
      margin-top: 5%
      color: $light
      font-size: 1.1em
      width: 85%
      height: $field_height*10.5
      align-self: flex-start
      display: flex
      flex-direction: column
      justify-content: space-around
      div
        text-align: right
        padding-right: 15%
      input
        width: $field_width/1.17
        background-color: #0000
        border: none
        border-bottom: 2px solid $light
        font-size: 1.1em
        color: $light
        &:disabled
          border: none
      textarea
        width: $field_width/1.17
        background-color: #0000
        border: none
        font-size: 0.9em
        color: $light
        resize: none
        text-align: center
      #finish
        padding-left: 30%
        display: flex
        justify-content: space-between
        button
          background-color: #0000
          border: none
          font-size: 2em
          transition: 0.7s
          &:hover
            transform: scale(1.3)
            cursor: pointer
          &:focus
            outline: none

</style>
