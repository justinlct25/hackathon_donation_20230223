# Hack The Diff 2023

# Importing the font

Importing a font in CSS:
```css
@font-face {
    font-family: MindMeridian-Regular;
    src: url(../fonts/MindMeridianW05-Regular.woff2) format("woff2"), url(../fonts/MindMeridianW05-Regular.woff) format("woff");
    font-display: swap
}

@font-face {
    font-family: MindMeridian-Display;
    src: url(../fonts/MindMeridianW05-Display.woff2) format("woff2"), url(../fonts/MindMeridianW05-Display.woff) format("woff");
    font-display: swap
}

@font-face {
    font-family: MindMeridian-Bold;
    src: url(../fonts/MindMeridianW05-Bold.woff2) format("woff2"), url(../fonts/MindMeridianW05-Bold.woff) format("woff");
    font-display: swap
}
```

CSS Example of how to use the font:
```css
body {
	font-family: "MindMeridian-Regular", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.bold {
	font-family: "MindMeridian-Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
}
```