/**
 * Waits for a specific text to appear in an element of the specified type.
 * @param text - The text to wait for.
 * @param elementType - The type of element to search for (default is 'div').
 * @returns A promise that resolves when the text appears.
 */
async function waitForTextToAppear(text, elementType = 'div') {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      // Search for the element containing the specified text
      const element = Array.from(document.querySelectorAll(elementType))
                    .find(el => el.textContent === text);
      if (element) {
        clearInterval(interval);
        resolve();
        return;
      }
    }, 100); // Check every 100ms
  });
}

/**
 * Waits for a specific text to disappear from an element of the specified type.
 * @param text - The text to wait for.
 * @param elementType - The type of element to search for (default is 'div').
 * @returns A promise that resolves when the text disappears.
 */
async function waitForTextToDisappear(text, elementType = 'div') {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      // Search for the element containing the specified text
      const element = Array.from(document.querySelectorAll(elementType))
                    .find(el => el.textContent === text);
      if (!element) {
        clearInterval(interval);
        resolve();
        return;
      }
    }, 100); // Check every 100ms
  });
}

/**
 * Delays execution for a specified number of milliseconds.
 * @param ms - The number of milliseconds to delay.
 * @returns A promise that resolves after the delay.
 */
async function delay(ms) {
  await new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Clicks the "Save" button on the page if it exists.
 */
function clickSaveButton() {
  const saveButton = document.querySelector('[data-value*="Save"]');
  if (!saveButton) {
    console.log('Save button not found');
    return;
  }

  console.log('Found save button:', saveButton);

  saveButton.click();
  console.log('Clicked save button');
}

/**
 * Processes a single restaurant element.
 * @param restaurant - The restaurant element to process.
 */
async function processRestaurant(restaurant: Element) {
  console.log('Processing restaurant:', restaurant);

  // Locate the button associated with the restaurant
  const button = restaurant.parentElement.parentElement.previousSibling;
  if (!button) {
    console.log('Button not found');
    return;
  }

  console.log('Found button:', button);

  // Locate the category span
  const categorySpan = button.querySelector('.fontBodyMedium > div:last-child > div:last-child span:last-child');
  if (!categorySpan) {
    console.log('Category span not found');
    return;
  }

  console.log('Found category span:', categorySpan);

  // Locate the restaurant name element
  const restaurantNameElement = button.querySelector('.fontHeadlineSmall');
  if (!restaurantNameElement) {
    console.log('Restaurant name element not found');
    return;
  }

  console.log('Found restaurant name element:', restaurantNameElement);

  // Click the button to open the restaurant details
  button.click();
  console.log('Clicked button');
  await delay(250);

  const restaurantName = restaurantNameElement.textContent;
  console.log('Restaurant name:', restaurantName);

  // Wait for the restaurant name to appear in the header
  await waitForTextToAppear(restaurantName, 'h1');
  console.log('H1 element found');
  await delay(250);

  // Click the "Save" button
  clickSaveButton();
  await delay(250);

  // Check if the restaurant is already marked as "Want to go"
  const wantToGoElement = Array.from(document.querySelectorAll('[aria-checked="true"] div'))
                    .find(el => el.textContent === 'Want to go');
  if (wantToGoElement) {
    console.log('Found "Want to go" element:', wantToGoElement);

    // Remove the "Want to go" mark
    wantToGoElement.parentElement.click();
    console.log('Clicked "Want to go" element');
    await delay(250);

    await waitForTextToAppear('Removing…');
    console.log('Removing…');
    await delay(250);

    await waitForTextToDisappear('Removing…');
    console.log('Removed from Want to go');
    await delay(250);
  }

  // Determine the target category for the restaurant
  const category = categorySpan.textContent.trim().replace('· ', '');
  console.log('Category:', category);

  const targetCategories = {
    'Cafe': 'Coffee',
    'Coffee shop': 'Coffee', 
    'Coffee': 'Coffee',
    'Espresso bar': 'Coffee',
    'Tea house': 'Tea',
    'Tea shop': 'Tea',
    'Tea store': 'Tea',
    'Chinese tea house': 'Tea',
    'Bakery': 'Bakery',
    'Pastry shop': 'Bakery',
    'Dessert': 'Dessert',
    'Dessert shop': 'Dessert',
    'Dessert restaurant': 'Dessert',
    'Japanese sweets restaurant': 'Dessert',
  };

  const targetCategory = targetCategories[category] || 'Food';
  console.log('Target category:', targetCategory);

  // If the restaurant is not marked as closed, save it to the target category
  if (!category.includes('closed')) {
    clickSaveButton();
    await delay(250);

    const targetElement = Array.from(document.querySelectorAll('[aria-checked="false"] div'))
                      .find(el => el.textContent === targetCategory);
    if (!targetElement) {
      console.log('Target element not found');
      return;
    }

    console.log('Found target element:', targetElement);

    targetElement.parentElement.click();
    console.log(`Clicked ${targetCategory}`);
    await delay(250);

    await waitForTextToAppear('Saving…');
    console.log('Saving…');
    await delay(250);

    await waitForTextToDisappear('Saving…');
    console.log(`Saved to ${targetCategory}`);
  }
  await delay(250);
}

/**
 * Processes all restaurants on the page.
 * Recursively calls itself to handle dynamic loading of restaurants.
 */
async function processRestaurants() {
  const restaurants: NodeListOf<Element> = document.querySelectorAll('[aria-label="Add note"]');
  console.log('Found restaurants:', restaurants.length);

  for (const restaurant of restaurants) {
    // Skip restaurants with broken images
    const parentElement = restaurant.parentElement;
    const grandParentElement = parentElement?.parentElement;
    const previousSibling = grandParentElement?.previousSibling as HTMLElement;

    const isBroken = previousSibling 
      ? Array.from(previousSibling.querySelectorAll('img'))
          .some(img => img.src === 'https://maps.gstatic.com/tactile/pane/result-no-thumbnail-2x.png')
      : false;

    if (isBroken) {
      continue;
    } else {
      await processRestaurant(restaurant);
      break; // Process one restaurant at a time
    }
  }

  // Recursively process the next batch of restaurants
  processRestaurants();
}

// Start processing restaurants
processRestaurants();