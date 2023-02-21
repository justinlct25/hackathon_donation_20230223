# Resources for Hack The Diff

## Font

Please use the "MindMeridian" font, found under resources/font/ in woff2 format.

*See the README in the font folder for instrucitons on how to use this font in your CSS.*

## Colours

Please use the following colours:

- ![#1300c1](https://placehold.co/15x15/f03c15/f03c15.png) `#1300c1` Blue
- ![#FFFFFF](https://placehold.co/15x15/FFFFFF/FFFFFF.png) `#FFFFFF` White
- ![#9DA8FF](https://placehold.co/15x15/9DA8FF/9DA8FF.png) `#9DA8FF` Sky
- ![#71F5C4](https://placehold.co/15x15/71F5C4/71F5C4.png) `#71F5C4` Green
- ![#8149FF](https://placehold.co/15x15/8149FF/8149FF.png) `#8149FF` Purple
- ![#FF0071](https://placehold.co/15x15/FF0071/FF0071.png) `#FF0071` Pink

You could use the hex colour codes as CSS variables like so:
```css
/* Define colours */
:root {
	--mind-blue: #1300c1;
	--mind-sky: #9DA8FF;
	--mind-green: #71F5C4;
	--mind-purple: #8149FF;
	--mind-pink: #FF0071;
}

/* Example of variable usage */
.text {
	color: var(--mind-purple);
}
```