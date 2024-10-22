
/**
 * Get recommended text color based on the brightness of the background color
 * @param {{ element: Element, black: string, white: string }} element
 * @returns {string}
 */
function getRecomendedTextColor({element, black = "black", white = "white"}) {
  // Get rgb color of the strip
  const rgbString = getComputedStyle(element).backgroundColor;

  // Convert rgb string to array
  const rgb = rgbString
    .slice(4, -1)
    .split(",")
    .map((value) => parseInt(value));

  // Calculate the brightness of the color
  const brightness = Math.round(
    (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
  );

  // Set the color of the icon based on the brightness
  return brightness > 125 ? black : white;
}
