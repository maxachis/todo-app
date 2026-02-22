<script lang="ts">
	type EmojiEntry = {
		emoji: string;
		name: string;
		keywords: string[];
	};

	type EmojiCategory = {
		category: string;
		values: EmojiEntry[];
	};

	const EMOJIS: EmojiCategory[] = [
		{
			category: 'Smileys',
			values: [
				{ emoji: '😀', name: 'grinning face', keywords: ['happy', 'smile', 'joy'] },
				{ emoji: '😃', name: 'grinning face big eyes', keywords: ['happy', 'excited'] },
				{ emoji: '😄', name: 'grinning squinting face', keywords: ['laugh', 'happy'] },
				{ emoji: '😁', name: 'beaming face', keywords: ['grin', 'happy'] },
				{ emoji: '😆', name: 'squinting face', keywords: ['laugh', 'lol'] },
				{ emoji: '😅', name: 'sweat smile', keywords: ['nervous', 'relief'] },
				{ emoji: '🤣', name: 'rofl', keywords: ['laugh', 'hilarious', 'lmao'] },
				{ emoji: '😂', name: 'joy', keywords: ['laugh', 'cry', 'tears'] },
				{ emoji: '🙂', name: 'slightly smiling', keywords: ['okay', 'fine'] },
				{ emoji: '😉', name: 'winking face', keywords: ['wink', 'playful'] },
				{ emoji: '😊', name: 'smiling blushing', keywords: ['blush', 'warm'] },
				{ emoji: '😇', name: 'smiling halo', keywords: ['angel', 'innocent'] },
				{ emoji: '🥰', name: 'smiling hearts', keywords: ['love', 'adore'] },
				{ emoji: '😍', name: 'heart eyes', keywords: ['love', 'crush'] },
				{ emoji: '🤩', name: 'star struck', keywords: ['excited', 'amazing'] },
				{ emoji: '😘', name: 'kissing heart', keywords: ['kiss', 'love'] },
				{ emoji: '😋', name: 'savoring face', keywords: ['yummy', 'delicious'] },
				{ emoji: '😜', name: 'winking tongue', keywords: ['silly', 'playful'] },
				{ emoji: '🤪', name: 'zany face', keywords: ['crazy', 'wild'] },
				{ emoji: '🤗', name: 'hugging face', keywords: ['hug', 'warm'] },
				{ emoji: '🤔', name: 'thinking face', keywords: ['think', 'hmm', 'consider'] },
				{ emoji: '🫡', name: 'saluting face', keywords: ['respect', 'yes sir'] },
				{ emoji: '🤫', name: 'shushing face', keywords: ['quiet', 'secret'] },
				{ emoji: '😶', name: 'no mouth', keywords: ['speechless', 'silent'] },
				{ emoji: '😏', name: 'smirking face', keywords: ['smirk', 'sly'] },
				{ emoji: '😌', name: 'relieved face', keywords: ['relief', 'calm'] },
				{ emoji: '😔', name: 'pensive face', keywords: ['sad', 'thoughtful'] },
				{ emoji: '😪', name: 'sleepy face', keywords: ['tired', 'sleep'] },
				{ emoji: '😴', name: 'sleeping face', keywords: ['zzz', 'asleep'] },
				{ emoji: '🤮', name: 'vomiting face', keywords: ['sick', 'gross'] },
				{ emoji: '🤧', name: 'sneezing face', keywords: ['sick', 'cold'] },
				{ emoji: '🥵', name: 'hot face', keywords: ['heat', 'sweat'] },
				{ emoji: '🥶', name: 'cold face', keywords: ['freezing', 'ice'] },
				{ emoji: '😵', name: 'dizzy face', keywords: ['confused', 'overwhelmed'] },
				{ emoji: '🤯', name: 'exploding head', keywords: ['mind blown', 'shocked'] },
				{ emoji: '😎', name: 'sunglasses face', keywords: ['cool', 'confident'] },
				{ emoji: '🥳', name: 'partying face', keywords: ['party', 'celebrate'] },
				{ emoji: '😤', name: 'huffing face', keywords: ['angry', 'frustrated'] },
				{ emoji: '😭', name: 'loudly crying', keywords: ['cry', 'sad', 'upset'] },
				{ emoji: '😱', name: 'screaming face', keywords: ['shock', 'fear'] },
				{ emoji: '😈', name: 'smiling imp', keywords: ['devil', 'mischief'] },
				{ emoji: '💀', name: 'skull', keywords: ['dead', 'dying', 'rip'] },
				{ emoji: '🤖', name: 'robot', keywords: ['bot', 'ai', 'machine'] },
				{ emoji: '👻', name: 'ghost', keywords: ['spooky', 'halloween'] },
				{ emoji: '🎃', name: 'jack-o-lantern', keywords: ['halloween', 'pumpkin'] },
				{ emoji: '🥸', name: 'disguised face', keywords: ['disguise', 'incognito'] },
				{ emoji: '🫠', name: 'melting face', keywords: ['melt', 'hot', 'overwhelmed'] },
				{ emoji: '🫣', name: 'peeking face', keywords: ['peek', 'shy', 'nervous'] }
			]
		},
		{
			category: 'Gestures & People',
			values: [
				{ emoji: '👋', name: 'waving hand', keywords: ['hello', 'bye', 'wave'] },
				{ emoji: '🤚', name: 'raised back of hand', keywords: ['stop', 'hand'] },
				{ emoji: '✋', name: 'raised hand', keywords: ['stop', 'high five'] },
				{ emoji: '🖖', name: 'vulcan salute', keywords: ['spock', 'trek'] },
				{ emoji: '👌', name: 'ok hand', keywords: ['okay', 'perfect'] },
				{ emoji: '🤌', name: 'pinched fingers', keywords: ['italian', 'chef kiss'] },
				{ emoji: '✌️', name: 'victory hand', keywords: ['peace', 'two'] },
				{ emoji: '🤞', name: 'crossed fingers', keywords: ['luck', 'hope'] },
				{ emoji: '🫰', name: 'hand with index and thumb crossed', keywords: ['money', 'snap'] },
				{ emoji: '🤙', name: 'call me hand', keywords: ['shaka', 'hang loose'] },
				{ emoji: '👈', name: 'pointing left', keywords: ['left', 'direction'] },
				{ emoji: '👉', name: 'pointing right', keywords: ['right', 'direction'] },
				{ emoji: '👆', name: 'pointing up', keywords: ['up', 'above'] },
				{ emoji: '👇', name: 'pointing down', keywords: ['down', 'below'] },
				{ emoji: '👍', name: 'thumbs up', keywords: ['like', 'approve', 'yes'] },
				{ emoji: '👎', name: 'thumbs down', keywords: ['dislike', 'no'] },
				{ emoji: '✊', name: 'raised fist', keywords: ['power', 'solidarity'] },
				{ emoji: '👊', name: 'oncoming fist', keywords: ['punch', 'bump'] },
				{ emoji: '🤝', name: 'handshake', keywords: ['deal', 'agreement'] },
				{ emoji: '🙏', name: 'folded hands', keywords: ['please', 'pray', 'thanks'] },
				{ emoji: '💪', name: 'flexed biceps', keywords: ['strong', 'muscle', 'power'] },
				{ emoji: '🫶', name: 'heart hands', keywords: ['love', 'heart', 'adore'] },
				{ emoji: '👀', name: 'eyes', keywords: ['look', 'see', 'watch'] },
				{ emoji: '👁️', name: 'eye', keywords: ['see', 'vision'] },
				{ emoji: '👅', name: 'tongue', keywords: ['taste', 'lick'] },
				{ emoji: '👄', name: 'mouth', keywords: ['lips', 'kiss'] },
				{ emoji: '🧠', name: 'brain', keywords: ['think', 'smart', 'mind'] },
				{ emoji: '👶', name: 'baby', keywords: ['infant', 'child'] },
				{ emoji: '👦', name: 'boy', keywords: ['kid', 'child'] },
				{ emoji: '👧', name: 'girl', keywords: ['kid', 'child'] },
				{ emoji: '👨', name: 'man', keywords: ['male', 'adult'] },
				{ emoji: '👩', name: 'woman', keywords: ['female', 'adult'] },
				{ emoji: '🧓', name: 'older person', keywords: ['elderly', 'senior'] },
				{ emoji: '👴', name: 'old man', keywords: ['grandpa', 'elder'] },
				{ emoji: '👵', name: 'old woman', keywords: ['grandma', 'elder'] },
				{ emoji: '👮', name: 'police officer', keywords: ['cop', 'law'] },
				{ emoji: '👷', name: 'construction worker', keywords: ['build', 'hard hat'] },
				{ emoji: '💂', name: 'guard', keywords: ['royal', 'british'] },
				{ emoji: '🕵️', name: 'detective', keywords: ['spy', 'investigate'] },
				{ emoji: '👩‍⚕️', name: 'health worker', keywords: ['doctor', 'nurse'] },
				{ emoji: '👩‍🍳', name: 'cook', keywords: ['chef', 'kitchen'] },
				{ emoji: '👩‍🎓', name: 'student', keywords: ['graduate', 'school'] },
				{ emoji: '👩‍🏫', name: 'teacher', keywords: ['professor', 'educate'] },
				{ emoji: '👩‍💻', name: 'technologist', keywords: ['coder', 'developer'] },
				{ emoji: '👩‍🚀', name: 'astronaut', keywords: ['space', 'nasa'] },
				{ emoji: '👩‍🎤', name: 'singer', keywords: ['musician', 'performer'] },
				{ emoji: '👩‍🎨', name: 'artist', keywords: ['painter', 'creative'] },
				{ emoji: '🧙', name: 'mage', keywords: ['wizard', 'magic'] },
				{ emoji: '🧛', name: 'vampire', keywords: ['dracula', 'halloween'] },
				{ emoji: '🧜', name: 'merperson', keywords: ['mermaid', 'sea'] },
				{ emoji: '🧚', name: 'fairy', keywords: ['magic', 'fantasy'] },
				{ emoji: '🧝', name: 'elf', keywords: ['fantasy', 'tolkien'] },
				{ emoji: '🧞', name: 'genie', keywords: ['wish', 'lamp'] },
				{ emoji: '🧟', name: 'zombie', keywords: ['undead', 'horror'] },
				{ emoji: '🧑‍🤝‍🧑', name: 'people holding hands', keywords: ['together', 'couple'] },
				{ emoji: '👪', name: 'family', keywords: ['home', 'parents', 'kids'] },
				{ emoji: '🫂', name: 'people hugging', keywords: ['hug', 'comfort'] }
			]
		},
		{
			category: 'Animals',
			values: [
				{ emoji: '🐶', name: 'dog face', keywords: ['puppy', 'pet'] },
				{ emoji: '🐱', name: 'cat face', keywords: ['kitty', 'pet'] },
				{ emoji: '🐭', name: 'mouse face', keywords: ['rodent', 'small'] },
				{ emoji: '🐹', name: 'hamster', keywords: ['pet', 'cute'] },
				{ emoji: '🐰', name: 'rabbit face', keywords: ['bunny', 'easter'] },
				{ emoji: '🦊', name: 'fox', keywords: ['clever', 'red'] },
				{ emoji: '🐻', name: 'bear', keywords: ['grizzly', 'teddy'] },
				{ emoji: '🐼', name: 'panda', keywords: ['bamboo', 'china'] },
				{ emoji: '🐻‍❄️', name: 'polar bear', keywords: ['arctic', 'ice'] },
				{ emoji: '🐨', name: 'koala', keywords: ['australia', 'eucalyptus'] },
				{ emoji: '🐯', name: 'tiger face', keywords: ['fierce', 'cat'] },
				{ emoji: '🦁', name: 'lion', keywords: ['king', 'pride'] },
				{ emoji: '🐮', name: 'cow face', keywords: ['farm', 'moo'] },
				{ emoji: '🐷', name: 'pig face', keywords: ['farm', 'oink'] },
				{ emoji: '🐸', name: 'frog', keywords: ['ribbit', 'green'] },
				{ emoji: '🐵', name: 'monkey face', keywords: ['primate', 'banana'] },
				{ emoji: '🙈', name: 'see-no-evil monkey', keywords: ['hide', 'shy'] },
				{ emoji: '🙉', name: 'hear-no-evil monkey', keywords: ['ignore', 'deaf'] },
				{ emoji: '🙊', name: 'speak-no-evil monkey', keywords: ['secret', 'quiet'] },
				{ emoji: '🐔', name: 'chicken', keywords: ['hen', 'farm'] },
				{ emoji: '🐧', name: 'penguin', keywords: ['arctic', 'cold'] },
				{ emoji: '🐦', name: 'bird', keywords: ['tweet', 'fly'] },
				{ emoji: '🦅', name: 'eagle', keywords: ['freedom', 'soar'] },
				{ emoji: '🦆', name: 'duck', keywords: ['quack', 'pond'] },
				{ emoji: '🦉', name: 'owl', keywords: ['wise', 'night'] },
				{ emoji: '🦇', name: 'bat', keywords: ['night', 'cave'] },
				{ emoji: '🐺', name: 'wolf', keywords: ['howl', 'pack'] },
				{ emoji: '🐗', name: 'boar', keywords: ['wild', 'pig'] },
				{ emoji: '🐴', name: 'horse face', keywords: ['pony', 'ride'] },
				{ emoji: '🦄', name: 'unicorn', keywords: ['magic', 'fantasy', 'rainbow'] },
				{ emoji: '🐝', name: 'honeybee', keywords: ['bee', 'honey', 'buzz'] },
				{ emoji: '🪱', name: 'worm', keywords: ['earth', 'garden'] },
				{ emoji: '🐛', name: 'bug', keywords: ['insect', 'caterpillar'] },
				{ emoji: '🦋', name: 'butterfly', keywords: ['pretty', 'metamorphosis'] },
				{ emoji: '🐌', name: 'snail', keywords: ['slow', 'shell'] },
				{ emoji: '🐙', name: 'octopus', keywords: ['tentacle', 'sea'] },
				{ emoji: '🦑', name: 'squid', keywords: ['ocean', 'ink'] },
				{ emoji: '🦐', name: 'shrimp', keywords: ['seafood', 'prawn'] },
				{ emoji: '🦀', name: 'crab', keywords: ['beach', 'pinch'] },
				{ emoji: '🐡', name: 'blowfish', keywords: ['puffer', 'ocean'] },
				{ emoji: '🐠', name: 'tropical fish', keywords: ['colorful', 'reef'] },
				{ emoji: '🐟', name: 'fish', keywords: ['swim', 'ocean'] },
				{ emoji: '🐬', name: 'dolphin', keywords: ['smart', 'ocean'] },
				{ emoji: '🐳', name: 'whale', keywords: ['ocean', 'big'] },
				{ emoji: '🦈', name: 'shark', keywords: ['ocean', 'teeth'] },
				{ emoji: '🐊', name: 'crocodile', keywords: ['alligator', 'reptile'] },
				{ emoji: '🐢', name: 'turtle', keywords: ['slow', 'shell'] },
				{ emoji: '🦎', name: 'lizard', keywords: ['reptile', 'gecko'] },
				{ emoji: '🐍', name: 'snake', keywords: ['python', 'slither'] },
				{ emoji: '🦕', name: 'sauropod', keywords: ['dinosaur', 'brontosaurus'] },
				{ emoji: '🦖', name: 't-rex', keywords: ['dinosaur', 'rawr'] },
				{ emoji: '🦩', name: 'flamingo', keywords: ['pink', 'tropical'] },
				{ emoji: '🦚', name: 'peacock', keywords: ['feather', 'fancy'] },
				{ emoji: '🦜', name: 'parrot', keywords: ['colorful', 'talk'] },
				{ emoji: '🦥', name: 'sloth', keywords: ['lazy', 'slow'] },
				{ emoji: '🦦', name: 'otter', keywords: ['cute', 'swim'] },
				{ emoji: '🦨', name: 'skunk', keywords: ['stink', 'spray'] },
				{ emoji: '🦘', name: 'kangaroo', keywords: ['australia', 'hop'] },
				{ emoji: '🦛', name: 'hippopotamus', keywords: ['hippo', 'big'] },
				{ emoji: '🦏', name: 'rhinoceros', keywords: ['horn', 'tough'] },
				{ emoji: '🐘', name: 'elephant', keywords: ['big', 'memory'] },
				{ emoji: '🦒', name: 'giraffe', keywords: ['tall', 'spots'] },
				{ emoji: '🐪', name: 'camel', keywords: ['desert', 'hump'] },
				{ emoji: '🦬', name: 'bison', keywords: ['buffalo', 'prairie'] },
				{ emoji: '🦣', name: 'mammoth', keywords: ['extinct', 'woolly'] },
				{ emoji: '🦫', name: 'beaver', keywords: ['dam', 'build'] },
				{ emoji: '🐿️', name: 'chipmunk', keywords: ['squirrel', 'nuts'] }
			]
		},
		{
			category: 'Nature',
			values: [
				{ emoji: '🌸', name: 'cherry blossom', keywords: ['flower', 'spring', 'pink'] },
				{ emoji: '🌹', name: 'rose', keywords: ['flower', 'love', 'red'] },
				{ emoji: '🌺', name: 'hibiscus', keywords: ['flower', 'tropical'] },
				{ emoji: '🌻', name: 'sunflower', keywords: ['flower', 'sun', 'happy'] },
				{ emoji: '🌼', name: 'blossom', keywords: ['flower', 'bloom'] },
				{ emoji: '🌷', name: 'tulip', keywords: ['flower', 'spring'] },
				{ emoji: '💐', name: 'bouquet', keywords: ['flowers', 'gift'] },
				{ emoji: '🌱', name: 'seedling', keywords: ['plant', 'grow', 'sprout'] },
				{ emoji: '🪴', name: 'potted plant', keywords: ['houseplant', 'green'] },
				{ emoji: '🌲', name: 'evergreen tree', keywords: ['pine', 'forest'] },
				{ emoji: '🌳', name: 'deciduous tree', keywords: ['tree', 'park'] },
				{ emoji: '🌴', name: 'palm tree', keywords: ['tropical', 'beach'] },
				{ emoji: '🌵', name: 'cactus', keywords: ['desert', 'prickly'] },
				{ emoji: '🍀', name: 'four leaf clover', keywords: ['lucky', 'irish'] },
				{ emoji: '🍁', name: 'maple leaf', keywords: ['fall', 'autumn', 'canada'] },
				{ emoji: '🍂', name: 'fallen leaf', keywords: ['autumn', 'fall'] },
				{ emoji: '🍃', name: 'leaf fluttering', keywords: ['wind', 'green'] },
				{ emoji: '🪹', name: 'empty nest', keywords: ['bird', 'home'] },
				{ emoji: '🪺', name: 'nest with eggs', keywords: ['bird', 'spring'] },
				{ emoji: '🍄', name: 'mushroom', keywords: ['fungi', 'forest'] },
				{ emoji: '🌰', name: 'chestnut', keywords: ['nut', 'autumn'] },
				{ emoji: '🌾', name: 'sheaf of rice', keywords: ['grain', 'harvest'] },
				{ emoji: '🪨', name: 'rock', keywords: ['stone', 'boulder'] },
				{ emoji: '🪵', name: 'wood', keywords: ['log', 'lumber'] },
				{ emoji: '🔥', name: 'fire', keywords: ['flame', 'hot', 'lit'] },
				{ emoji: '💧', name: 'droplet', keywords: ['water', 'rain'] },
				{ emoji: '🌊', name: 'wave', keywords: ['ocean', 'sea', 'surf'] }
			]
		},
		{
			category: 'Weather',
			values: [
				{ emoji: '☀️', name: 'sun', keywords: ['sunny', 'bright', 'warm'] },
				{ emoji: '🌤️', name: 'sun behind small cloud', keywords: ['partly sunny'] },
				{ emoji: '⛅', name: 'sun behind cloud', keywords: ['partly cloudy'] },
				{ emoji: '🌥️', name: 'sun behind large cloud', keywords: ['mostly cloudy'] },
				{ emoji: '☁️', name: 'cloud', keywords: ['cloudy', 'overcast'] },
				{ emoji: '🌦️', name: 'sun behind rain cloud', keywords: ['rain', 'sun shower'] },
				{ emoji: '🌧️', name: 'cloud with rain', keywords: ['rainy', 'wet'] },
				{ emoji: '⛈️', name: 'cloud with lightning and rain', keywords: ['thunderstorm'] },
				{ emoji: '🌩️', name: 'cloud with lightning', keywords: ['thunder', 'storm'] },
				{ emoji: '❄️', name: 'snowflake', keywords: ['snow', 'cold', 'winter'] },
				{ emoji: '☃️', name: 'snowman', keywords: ['winter', 'snow'] },
				{ emoji: '🌨️', name: 'cloud with snow', keywords: ['snowy', 'blizzard'] },
				{ emoji: '🌪️', name: 'tornado', keywords: ['twister', 'storm'] },
				{ emoji: '🌫️', name: 'fog', keywords: ['misty', 'haze'] },
				{ emoji: '🌈', name: 'rainbow', keywords: ['colorful', 'hope'] },
				{ emoji: '⭐', name: 'star', keywords: ['night', 'bright'] },
				{ emoji: '🌟', name: 'glowing star', keywords: ['sparkle', 'shine'] },
				{ emoji: '✨', name: 'sparkles', keywords: ['magic', 'clean', 'new'] },
				{ emoji: '💫', name: 'dizzy', keywords: ['star', 'shooting'] },
				{ emoji: '🌙', name: 'crescent moon', keywords: ['night', 'sleep'] },
				{ emoji: '🌕', name: 'full moon', keywords: ['night', 'bright'] },
				{ emoji: '🌑', name: 'new moon', keywords: ['dark', 'night'] }
			]
		},
		{
			category: 'Food & Drink',
			values: [
				{ emoji: '🍎', name: 'red apple', keywords: ['fruit', 'healthy'] },
				{ emoji: '🍊', name: 'tangerine', keywords: ['orange', 'citrus'] },
				{ emoji: '🍋', name: 'lemon', keywords: ['citrus', 'sour'] },
				{ emoji: '🍌', name: 'banana', keywords: ['fruit', 'yellow'] },
				{ emoji: '🍉', name: 'watermelon', keywords: ['fruit', 'summer'] },
				{ emoji: '🍇', name: 'grapes', keywords: ['fruit', 'wine'] },
				{ emoji: '🍓', name: 'strawberry', keywords: ['fruit', 'berry'] },
				{ emoji: '🫐', name: 'blueberries', keywords: ['fruit', 'berry'] },
				{ emoji: '🍑', name: 'peach', keywords: ['fruit', 'fuzzy'] },
				{ emoji: '🥭', name: 'mango', keywords: ['fruit', 'tropical'] },
				{ emoji: '🍍', name: 'pineapple', keywords: ['fruit', 'tropical'] },
				{ emoji: '🥥', name: 'coconut', keywords: ['tropical', 'palm'] },
				{ emoji: '🥑', name: 'avocado', keywords: ['guacamole', 'green'] },
				{ emoji: '🍆', name: 'eggplant', keywords: ['vegetable', 'purple'] },
				{ emoji: '🥦', name: 'broccoli', keywords: ['vegetable', 'green'] },
				{ emoji: '🥬', name: 'leafy green', keywords: ['lettuce', 'salad'] },
				{ emoji: '🌽', name: 'corn', keywords: ['maize', 'vegetable'] },
				{ emoji: '🌶️', name: 'hot pepper', keywords: ['spicy', 'chili'] },
				{ emoji: '🥕', name: 'carrot', keywords: ['vegetable', 'orange'] },
				{ emoji: '🧄', name: 'garlic', keywords: ['flavor', 'cooking'] },
				{ emoji: '🧅', name: 'onion', keywords: ['cooking', 'cry'] },
				{ emoji: '🥔', name: 'potato', keywords: ['vegetable', 'starch'] },
				{ emoji: '🍞', name: 'bread', keywords: ['toast', 'bakery'] },
				{ emoji: '🥐', name: 'croissant', keywords: ['pastry', 'french'] },
				{ emoji: '🧇', name: 'waffle', keywords: ['breakfast', 'syrup'] },
				{ emoji: '🥞', name: 'pancakes', keywords: ['breakfast', 'stack'] },
				{ emoji: '🧀', name: 'cheese', keywords: ['dairy', 'cheddar'] },
				{ emoji: '🍖', name: 'meat on bone', keywords: ['meat', 'bbq'] },
				{ emoji: '🍗', name: 'poultry leg', keywords: ['chicken', 'drumstick'] },
				{ emoji: '🥩', name: 'cut of meat', keywords: ['steak', 'beef'] },
				{ emoji: '🌭', name: 'hot dog', keywords: ['sausage', 'bbq'] },
				{ emoji: '🍔', name: 'hamburger', keywords: ['burger', 'fast food'] },
				{ emoji: '🍟', name: 'french fries', keywords: ['chips', 'fast food'] },
				{ emoji: '🍕', name: 'pizza', keywords: ['slice', 'italian'] },
				{ emoji: '🌮', name: 'taco', keywords: ['mexican', 'food'] },
				{ emoji: '🌯', name: 'burrito', keywords: ['wrap', 'mexican'] },
				{ emoji: '🥗', name: 'green salad', keywords: ['healthy', 'bowl'] },
				{ emoji: '🍜', name: 'steaming bowl', keywords: ['ramen', 'noodles', 'soup'] },
				{ emoji: '🍝', name: 'spaghetti', keywords: ['pasta', 'italian'] },
				{ emoji: '🍣', name: 'sushi', keywords: ['japanese', 'fish'] },
				{ emoji: '🍱', name: 'bento box', keywords: ['japanese', 'lunch'] },
				{ emoji: '🥟', name: 'dumpling', keywords: ['gyoza', 'dim sum'] },
				{ emoji: '🍳', name: 'cooking', keywords: ['egg', 'fry', 'breakfast'] },
				{ emoji: '🧁', name: 'cupcake', keywords: ['dessert', 'sweet'] },
				{ emoji: '🎂', name: 'birthday cake', keywords: ['cake', 'party'] },
				{ emoji: '🍰', name: 'shortcake', keywords: ['dessert', 'slice'] },
				{ emoji: '🍩', name: 'doughnut', keywords: ['donut', 'sweet'] },
				{ emoji: '🍪', name: 'cookie', keywords: ['biscuit', 'sweet'] },
				{ emoji: '🍫', name: 'chocolate bar', keywords: ['candy', 'sweet'] },
				{ emoji: '🍬', name: 'candy', keywords: ['sweet', 'sugar'] },
				{ emoji: '🍭', name: 'lollipop', keywords: ['candy', 'sweet'] },
				{ emoji: '🍦', name: 'soft ice cream', keywords: ['dessert', 'cone'] },
				{ emoji: '☕', name: 'hot beverage', keywords: ['coffee', 'tea'] },
				{ emoji: '🍵', name: 'teacup', keywords: ['tea', 'green tea'] },
				{ emoji: '🧋', name: 'bubble tea', keywords: ['boba', 'milk tea'] },
				{ emoji: '🥤', name: 'cup with straw', keywords: ['soda', 'drink'] },
				{ emoji: '🧃', name: 'juice box', keywords: ['juice', 'drink'] },
				{ emoji: '🍺', name: 'beer mug', keywords: ['beer', 'drink', 'pub'] },
				{ emoji: '🍻', name: 'clinking beers', keywords: ['cheers', 'toast'] },
				{ emoji: '🥂', name: 'clinking glasses', keywords: ['champagne', 'celebrate'] },
				{ emoji: '🍷', name: 'wine glass', keywords: ['wine', 'drink'] },
				{ emoji: '🍸', name: 'cocktail glass', keywords: ['martini', 'drink'] },
				{ emoji: '🍹', name: 'tropical drink', keywords: ['cocktail', 'beach'] },
				{ emoji: '🧊', name: 'ice', keywords: ['cold', 'cube'] }
			]
		},
		{
			category: 'Activities & Sports',
			values: [
				{ emoji: '⚽', name: 'soccer ball', keywords: ['football', 'sport'] },
				{ emoji: '🏀', name: 'basketball', keywords: ['sport', 'hoop'] },
				{ emoji: '🏈', name: 'american football', keywords: ['sport', 'nfl'] },
				{ emoji: '⚾', name: 'baseball', keywords: ['sport', 'mlb'] },
				{ emoji: '🥎', name: 'softball', keywords: ['sport', 'ball'] },
				{ emoji: '🎾', name: 'tennis', keywords: ['sport', 'racket'] },
				{ emoji: '🏐', name: 'volleyball', keywords: ['sport', 'beach'] },
				{ emoji: '🏉', name: 'rugby', keywords: ['sport', 'ball'] },
				{ emoji: '🥏', name: 'flying disc', keywords: ['frisbee', 'ultimate'] },
				{ emoji: '🎱', name: 'pool 8 ball', keywords: ['billiards', 'game'] },
				{ emoji: '🏓', name: 'ping pong', keywords: ['table tennis', 'sport'] },
				{ emoji: '🏸', name: 'badminton', keywords: ['shuttlecock', 'sport'] },
				{ emoji: '🏒', name: 'ice hockey', keywords: ['sport', 'puck'] },
				{ emoji: '⛳', name: 'flag in hole', keywords: ['golf', 'sport'] },
				{ emoji: '🏹', name: 'bow and arrow', keywords: ['archery', 'target'] },
				{ emoji: '🎣', name: 'fishing pole', keywords: ['fish', 'hobby'] },
				{ emoji: '🥊', name: 'boxing glove', keywords: ['fight', 'sport'] },
				{ emoji: '🥋', name: 'martial arts', keywords: ['karate', 'judo'] },
				{ emoji: '🏋️', name: 'weight lifting', keywords: ['gym', 'exercise'] },
				{ emoji: '🚴', name: 'person biking', keywords: ['cycling', 'ride'] },
				{ emoji: '🏃', name: 'person running', keywords: ['jog', 'exercise'] },
				{ emoji: '🧗', name: 'person climbing', keywords: ['rock climbing', 'boulder'] },
				{ emoji: '🏊', name: 'person swimming', keywords: ['swim', 'pool'] },
				{ emoji: '🏄', name: 'person surfing', keywords: ['surf', 'wave'] },
				{ emoji: '🚣', name: 'person rowing', keywords: ['boat', 'row'] },
				{ emoji: '🧘', name: 'person in lotus', keywords: ['yoga', 'meditation'] },
				{ emoji: '⛷️', name: 'skier', keywords: ['ski', 'snow', 'winter'] },
				{ emoji: '🏂', name: 'snowboarder', keywords: ['snowboard', 'winter'] },
				{ emoji: '⛸️', name: 'ice skate', keywords: ['skating', 'winter'] },
				{ emoji: '🛹', name: 'skateboard', keywords: ['skate', 'trick'] },
				{ emoji: '🛷', name: 'sled', keywords: ['snow', 'winter'] },
				{ emoji: '🎿', name: 'skis', keywords: ['skiing', 'snow'] },
				{ emoji: '🏆', name: 'trophy', keywords: ['win', 'champion', 'award'] },
				{ emoji: '🥇', name: 'gold medal', keywords: ['first', 'winner'] },
				{ emoji: '🥈', name: 'silver medal', keywords: ['second', 'runner up'] },
				{ emoji: '🥉', name: 'bronze medal', keywords: ['third', 'place'] },
				{ emoji: '🏅', name: 'sports medal', keywords: ['award', 'achievement'] },
				{ emoji: '🎖️', name: 'military medal', keywords: ['honor', 'service'] },
				{ emoji: '🎪', name: 'circus tent', keywords: ['carnival', 'show'] },
				{ emoji: '🤹', name: 'person juggling', keywords: ['circus', 'multitask'] }
			]
		},
		{
			category: 'Arts & Entertainment',
			values: [
				{ emoji: '🎨', name: 'artist palette', keywords: ['art', 'paint', 'creative'] },
				{ emoji: '🖌️', name: 'paintbrush', keywords: ['art', 'paint'] },
				{ emoji: '🖍️', name: 'crayon', keywords: ['draw', 'color'] },
				{ emoji: '✏️', name: 'pencil', keywords: ['write', 'draw'] },
				{ emoji: '🖊️', name: 'pen', keywords: ['write', 'sign'] },
				{ emoji: '🎭', name: 'performing arts', keywords: ['theater', 'drama'] },
				{ emoji: '🎬', name: 'clapper board', keywords: ['movie', 'film', 'cinema'] },
				{ emoji: '📷', name: 'camera', keywords: ['photo', 'picture'] },
				{ emoji: '📸', name: 'camera with flash', keywords: ['photo', 'selfie'] },
				{ emoji: '📹', name: 'video camera', keywords: ['film', 'record'] },
				{ emoji: '🎥', name: 'movie camera', keywords: ['film', 'cinema'] },
				{ emoji: '📽️', name: 'film projector', keywords: ['movie', 'cinema'] },
				{ emoji: '🎵', name: 'musical note', keywords: ['music', 'song'] },
				{ emoji: '🎶', name: 'musical notes', keywords: ['music', 'melody'] },
				{ emoji: '🎤', name: 'microphone', keywords: ['sing', 'karaoke'] },
				{ emoji: '🎧', name: 'headphone', keywords: ['music', 'listen'] },
				{ emoji: '🎸', name: 'guitar', keywords: ['music', 'rock'] },
				{ emoji: '🎹', name: 'musical keyboard', keywords: ['piano', 'keys'] },
				{ emoji: '🥁', name: 'drum', keywords: ['beat', 'music'] },
				{ emoji: '🎺', name: 'trumpet', keywords: ['brass', 'music'] },
				{ emoji: '🎻', name: 'violin', keywords: ['strings', 'classical'] },
				{ emoji: '🪕', name: 'banjo', keywords: ['country', 'folk'] },
				{ emoji: '🎮', name: 'video game', keywords: ['gaming', 'controller'] },
				{ emoji: '🕹️', name: 'joystick', keywords: ['arcade', 'game'] },
				{ emoji: '🎲', name: 'game die', keywords: ['dice', 'chance', 'random'] },
				{ emoji: '🧩', name: 'puzzle piece', keywords: ['jigsaw', 'solve'] },
				{ emoji: '♟️', name: 'chess pawn', keywords: ['chess', 'strategy'] },
				{ emoji: '🎯', name: 'bullseye', keywords: ['target', 'dart', 'goal'] },
				{ emoji: '🎰', name: 'slot machine', keywords: ['casino', 'luck'] },
				{ emoji: '🎳', name: 'bowling', keywords: ['bowl', 'pins'] },
				{ emoji: '🎴', name: 'flower playing cards', keywords: ['card', 'game'] },
				{ emoji: '🃏', name: 'joker', keywords: ['card', 'wild'] }
			]
		},
		{
			category: 'Travel & Transport',
			values: [
				{ emoji: '✈️', name: 'airplane', keywords: ['flight', 'travel'] },
				{ emoji: '🚀', name: 'rocket', keywords: ['launch', 'space'] },
				{ emoji: '🛸', name: 'flying saucer', keywords: ['ufo', 'alien'] },
				{ emoji: '🚁', name: 'helicopter', keywords: ['fly', 'chopper'] },
				{ emoji: '🚗', name: 'car', keywords: ['drive', 'automobile'] },
				{ emoji: '🚕', name: 'taxi', keywords: ['cab', 'ride'] },
				{ emoji: '🚌', name: 'bus', keywords: ['transit', 'transport'] },
				{ emoji: '🚎', name: 'trolleybus', keywords: ['transit', 'electric'] },
				{ emoji: '🚐', name: 'minibus', keywords: ['van', 'transport'] },
				{ emoji: '🚑', name: 'ambulance', keywords: ['emergency', 'medical'] },
				{ emoji: '🚒', name: 'fire engine', keywords: ['fire', 'emergency'] },
				{ emoji: '🚓', name: 'police car', keywords: ['cop', 'law'] },
				{ emoji: '🚚', name: 'delivery truck', keywords: ['shipping', 'move'] },
				{ emoji: '🚛', name: 'articulated lorry', keywords: ['truck', 'haul'] },
				{ emoji: '🚜', name: 'tractor', keywords: ['farm', 'field'] },
				{ emoji: '🏎️', name: 'racing car', keywords: ['fast', 'race', 'f1'] },
				{ emoji: '🏍️', name: 'motorcycle', keywords: ['bike', 'ride'] },
				{ emoji: '🛵', name: 'motor scooter', keywords: ['vespa', 'ride'] },
				{ emoji: '🚲', name: 'bicycle', keywords: ['bike', 'cycle'] },
				{ emoji: '🛴', name: 'kick scooter', keywords: ['scooter', 'ride'] },
				{ emoji: '🚂', name: 'locomotive', keywords: ['train', 'steam'] },
				{ emoji: '🚆', name: 'train', keywords: ['rail', 'commute'] },
				{ emoji: '🚇', name: 'metro', keywords: ['subway', 'underground'] },
				{ emoji: '🚢', name: 'ship', keywords: ['boat', 'cruise'] },
				{ emoji: '⛵', name: 'sailboat', keywords: ['sail', 'wind'] },
				{ emoji: '🛥️', name: 'motor boat', keywords: ['speedboat', 'lake'] },
				{ emoji: '🚤', name: 'speedboat', keywords: ['fast', 'water'] },
				{ emoji: '⛽', name: 'fuel pump', keywords: ['gas', 'petrol'] },
				{ emoji: '🗺️', name: 'world map', keywords: ['travel', 'explore'] },
				{ emoji: '🧳', name: 'luggage', keywords: ['travel', 'pack'] },
				{ emoji: '🗿', name: 'moai', keywords: ['easter island', 'statue'] },
				{ emoji: '🗽', name: 'statue of liberty', keywords: ['new york', 'usa'] },
				{ emoji: '🗼', name: 'tokyo tower', keywords: ['japan', 'landmark'] },
				{ emoji: '🏰', name: 'castle', keywords: ['medieval', 'fairy tale'] },
				{ emoji: '🕌', name: 'mosque', keywords: ['islam', 'religion'] },
				{ emoji: '🛕', name: 'hindu temple', keywords: ['temple', 'religion'] },
				{ emoji: '⛩️', name: 'shinto shrine', keywords: ['japan', 'torii'] },
				{ emoji: '🏝️', name: 'desert island', keywords: ['tropical', 'paradise'] },
				{ emoji: '🏖️', name: 'beach', keywords: ['vacation', 'summer'] },
				{ emoji: '🏔️', name: 'snow mountain', keywords: ['peak', 'hike'] },
				{ emoji: '⛰️', name: 'mountain', keywords: ['hike', 'climb'] },
				{ emoji: '🌋', name: 'volcano', keywords: ['lava', 'erupt'] },
				{ emoji: '🏕️', name: 'camping', keywords: ['tent', 'outdoor'] },
				{ emoji: '🏨', name: 'hotel', keywords: ['stay', 'lodging'] },
				{ emoji: '🌅', name: 'sunrise', keywords: ['morning', 'dawn'] },
				{ emoji: '🌄', name: 'sunrise over mountains', keywords: ['dawn', 'hike'] },
				{ emoji: '🌆', name: 'cityscape at dusk', keywords: ['city', 'evening'] },
				{ emoji: '🌇', name: 'sunset', keywords: ['evening', 'dusk'] },
				{ emoji: '🌃', name: 'night with stars', keywords: ['city', 'night'] },
				{ emoji: '🌉', name: 'bridge at night', keywords: ['city', 'landmark'] }
			]
		},
		{
			category: 'Productivity',
			values: [
				{ emoji: '📝', name: 'memo', keywords: ['write', 'notes', 'draft'] },
				{ emoji: '✅', name: 'check mark', keywords: ['done', 'complete', 'success'] },
				{ emoji: '📅', name: 'calendar', keywords: ['schedule', 'date', 'plan'] },
				{ emoji: '🗓️', name: 'spiral calendar', keywords: ['events', 'plans'] },
				{ emoji: '⏰', name: 'alarm clock', keywords: ['reminder', 'time', 'deadline'] },
				{ emoji: '⏱️', name: 'stopwatch', keywords: ['timer', 'speed'] },
				{ emoji: '⏳', name: 'hourglass', keywords: ['timebox', 'timer', 'focus'] },
				{ emoji: '📌', name: 'pushpin', keywords: ['pin', 'important', 'mark'] },
				{ emoji: '📎', name: 'paperclip', keywords: ['attach', 'file', 'document'] },
				{ emoji: '📏', name: 'straight ruler', keywords: ['measure', 'length'] },
				{ emoji: '📐', name: 'triangular ruler', keywords: ['angle', 'geometry'] },
				{ emoji: '📈', name: 'chart increasing', keywords: ['growth', 'metrics', 'analytics'] },
				{ emoji: '📉', name: 'chart decreasing', keywords: ['decline', 'loss'] },
				{ emoji: '📊', name: 'bar chart', keywords: ['report', 'stats', 'dashboard'] },
				{ emoji: '📋', name: 'clipboard', keywords: ['checklist', 'tasks'] },
				{ emoji: '📁', name: 'file folder', keywords: ['files', 'organize'] },
				{ emoji: '📂', name: 'open file folder', keywords: ['browse', 'documents'] },
				{ emoji: '🗂️', name: 'card index dividers', keywords: ['organize', 'sort'] },
				{ emoji: '🗃️', name: 'card file box', keywords: ['archive', 'storage'] },
				{ emoji: '🗑️', name: 'wastebasket', keywords: ['delete', 'trash'] },
				{ emoji: '📢', name: 'loudspeaker', keywords: ['announce', 'broadcast'] },
				{ emoji: '💡', name: 'light bulb', keywords: ['idea', 'brainstorm'] },
				{ emoji: '📦', name: 'package', keywords: ['ship', 'deliver'] },
				{ emoji: '🏷️', name: 'label', keywords: ['tag', 'price', 'category'] },
				{ emoji: '🔖', name: 'bookmark', keywords: ['save', 'mark', 'favorite'] }
			]
		},
		{
			category: 'Technology',
			values: [
				{ emoji: '💻', name: 'laptop', keywords: ['computer', 'coding'] },
				{ emoji: '🖥️', name: 'desktop computer', keywords: ['pc', 'workstation'] },
				{ emoji: '🖨️', name: 'printer', keywords: ['print', 'paper'] },
				{ emoji: '⌨️', name: 'keyboard', keywords: ['type', 'input'] },
				{ emoji: '🖱️', name: 'computer mouse', keywords: ['click', 'cursor'] },
				{ emoji: '💾', name: 'floppy disk', keywords: ['save', 'storage'] },
				{ emoji: '💿', name: 'optical disk', keywords: ['cd', 'disc'] },
				{ emoji: '📀', name: 'dvd', keywords: ['disc', 'media'] },
				{ emoji: '🔌', name: 'electric plug', keywords: ['power', 'connect'] },
				{ emoji: '🔋', name: 'battery', keywords: ['power', 'charge'] },
				{ emoji: '📱', name: 'mobile phone', keywords: ['cell', 'smartphone'] },
				{ emoji: '📲', name: 'mobile with arrow', keywords: ['download', 'call'] },
				{ emoji: '☎️', name: 'telephone', keywords: ['phone', 'call'] },
				{ emoji: '📞', name: 'telephone receiver', keywords: ['call', 'phone'] },
				{ emoji: '📟', name: 'pager', keywords: ['beep', 'retro'] },
				{ emoji: '📠', name: 'fax machine', keywords: ['fax', 'office'] },
				{ emoji: '📺', name: 'television', keywords: ['tv', 'watch'] },
				{ emoji: '📻', name: 'radio', keywords: ['listen', 'broadcast'] },
				{ emoji: '🎙️', name: 'studio microphone', keywords: ['podcast', 'record'] },
				{ emoji: '📡', name: 'satellite antenna', keywords: ['signal', 'broadcast'] },
				{ emoji: '🔭', name: 'telescope', keywords: ['observe', 'space'] },
				{ emoji: '🔬', name: 'microscope', keywords: ['science', 'research'] },
				{ emoji: '🧪', name: 'test tube', keywords: ['science', 'experiment'] },
				{ emoji: '🧫', name: 'petri dish', keywords: ['biology', 'lab'] },
				{ emoji: '🧬', name: 'dna', keywords: ['genetics', 'science'] },
				{ emoji: '⚙️', name: 'gear', keywords: ['settings', 'config'] },
				{ emoji: '🔧', name: 'wrench', keywords: ['fix', 'tool'] },
				{ emoji: '🔩', name: 'nut and bolt', keywords: ['hardware', 'build'] },
				{ emoji: '🛠️', name: 'hammer and wrench', keywords: ['tools', 'fix'] },
				{ emoji: '⛏️', name: 'pick', keywords: ['mine', 'dig'] },
				{ emoji: '🔗', name: 'link', keywords: ['chain', 'url', 'connect'] },
				{ emoji: '🧲', name: 'magnet', keywords: ['attract', 'magnetic'] }
			]
		},
		{
			category: 'Work & Finance',
			values: [
				{ emoji: '💼', name: 'briefcase', keywords: ['office', 'job', 'career'] },
				{ emoji: '🏢', name: 'office building', keywords: ['company', 'business'] },
				{ emoji: '🏭', name: 'factory', keywords: ['manufacturing', 'industry'] },
				{ emoji: '🏗️', name: 'building construction', keywords: ['build', 'develop'] },
				{ emoji: '🏛️', name: 'classical building', keywords: ['government', 'bank'] },
				{ emoji: '🏦', name: 'bank', keywords: ['money', 'finance'] },
				{ emoji: '💰', name: 'money bag', keywords: ['rich', 'cash'] },
				{ emoji: '💵', name: 'dollar', keywords: ['money', 'cash', 'usd'] },
				{ emoji: '💴', name: 'yen', keywords: ['money', 'japan'] },
				{ emoji: '💶', name: 'euro', keywords: ['money', 'europe'] },
				{ emoji: '💷', name: 'pound', keywords: ['money', 'british'] },
				{ emoji: '💳', name: 'credit card', keywords: ['pay', 'purchase'] },
				{ emoji: '💎', name: 'gem stone', keywords: ['diamond', 'precious'] },
				{ emoji: '⚖️', name: 'balance scale', keywords: ['justice', 'law', 'weigh'] },
				{ emoji: '🧾', name: 'receipt', keywords: ['bill', 'expenses'] },
				{ emoji: '📧', name: 'email', keywords: ['mail', 'message'] },
				{ emoji: '📨', name: 'incoming envelope', keywords: ['receive', 'mail'] },
				{ emoji: '📩', name: 'envelope with arrow', keywords: ['send', 'email'] },
				{ emoji: '📬', name: 'open mailbox', keywords: ['mail', 'postal'] },
				{ emoji: '🪪', name: 'identification card', keywords: ['id', 'badge'] },
				{ emoji: '👔', name: 'necktie', keywords: ['formal', 'business'] },
				{ emoji: '👥', name: 'busts in silhouette', keywords: ['team', 'people'] },
				{ emoji: '🤝', name: 'handshake', keywords: ['deal', 'agreement'] },
				{ emoji: '📃', name: 'page with curl', keywords: ['document', 'contract'] },
				{ emoji: '📄', name: 'page facing up', keywords: ['document', 'file'] },
				{ emoji: '📑', name: 'bookmark tabs', keywords: ['tabs', 'reference'] }
			]
		},
		{
			category: 'Home & Tools',
			values: [
				{ emoji: '🏠', name: 'house', keywords: ['home', 'family'] },
				{ emoji: '🏡', name: 'house with garden', keywords: ['home', 'yard'] },
				{ emoji: '🏘️', name: 'houses', keywords: ['neighborhood', 'suburb'] },
				{ emoji: '🛏️', name: 'bed', keywords: ['sleep', 'bedroom'] },
				{ emoji: '🛋️', name: 'couch and lamp', keywords: ['living room', 'relax'] },
				{ emoji: '🚿', name: 'shower', keywords: ['bath', 'wash'] },
				{ emoji: '🛁', name: 'bathtub', keywords: ['bath', 'relax'] },
				{ emoji: '🪑', name: 'chair', keywords: ['seat', 'sit'] },
				{ emoji: '🚪', name: 'door', keywords: ['entry', 'exit'] },
				{ emoji: '🪟', name: 'window', keywords: ['glass', 'view'] },
				{ emoji: '🪞', name: 'mirror', keywords: ['reflect', 'glass'] },
				{ emoji: '🧹', name: 'broom', keywords: ['clean', 'sweep'] },
				{ emoji: '🧺', name: 'basket', keywords: ['laundry', 'storage'] },
				{ emoji: '🧼', name: 'soap', keywords: ['clean', 'wash'] },
				{ emoji: '🪣', name: 'bucket', keywords: ['pail', 'water'] },
				{ emoji: '🧴', name: 'lotion bottle', keywords: ['cream', 'skincare'] },
				{ emoji: '🔑', name: 'key', keywords: ['lock', 'access'] },
				{ emoji: '🗝️', name: 'old key', keywords: ['vintage', 'unlock'] },
				{ emoji: '🔒', name: 'locked', keywords: ['secure', 'private'] },
				{ emoji: '🔓', name: 'unlocked', keywords: ['open', 'access'] },
				{ emoji: '🔨', name: 'hammer', keywords: ['build', 'nail'] },
				{ emoji: '🪛', name: 'screwdriver', keywords: ['fix', 'tool'] },
				{ emoji: '🪚', name: 'carpentry saw', keywords: ['cut', 'wood'] },
				{ emoji: '🔧', name: 'wrench', keywords: ['fix', 'plumbing'] },
				{ emoji: '🪜', name: 'ladder', keywords: ['climb', 'reach'] },
				{ emoji: '🧰', name: 'toolbox', keywords: ['tools', 'fix'] },
				{ emoji: '🪤', name: 'mouse trap', keywords: ['catch', 'pest'] },
				{ emoji: '🧲', name: 'magnet', keywords: ['attract', 'stick'] },
				{ emoji: '🪫', name: 'low battery', keywords: ['dead', 'charge'] },
				{ emoji: '💡', name: 'light bulb', keywords: ['lamp', 'bright'] },
				{ emoji: '🔦', name: 'flashlight', keywords: ['torch', 'light'] },
				{ emoji: '🕯️', name: 'candle', keywords: ['light', 'flame'] }
			]
		},
		{
			category: 'Health & Fitness',
			values: [
				{ emoji: '🏃', name: 'person running', keywords: ['exercise', 'cardio'] },
				{ emoji: '🚴', name: 'person biking', keywords: ['cycle', 'ride'] },
				{ emoji: '🏋️', name: 'weight lifting', keywords: ['gym', 'strength'] },
				{ emoji: '🧘', name: 'lotus position', keywords: ['yoga', 'meditation'] },
				{ emoji: '🏊', name: 'person swimming', keywords: ['swim', 'pool'] },
				{ emoji: '🧗', name: 'person climbing', keywords: ['climb', 'boulder'] },
				{ emoji: '🤸', name: 'person cartwheeling', keywords: ['gymnastics', 'acrobat'] },
				{ emoji: '⛹️', name: 'person bouncing ball', keywords: ['basketball', 'sport'] },
				{ emoji: '💊', name: 'pill', keywords: ['medicine', 'meds'] },
				{ emoji: '🩺', name: 'stethoscope', keywords: ['doctor', 'checkup'] },
				{ emoji: '🩹', name: 'adhesive bandage', keywords: ['bandaid', 'wound'] },
				{ emoji: '🩻', name: 'x-ray', keywords: ['medical', 'scan'] },
				{ emoji: '🩸', name: 'drop of blood', keywords: ['blood', 'test'] },
				{ emoji: '💉', name: 'syringe', keywords: ['vaccine', 'shot'] },
				{ emoji: '🏥', name: 'hospital', keywords: ['medical', 'health'] },
				{ emoji: '🧬', name: 'dna', keywords: ['genetics', 'biology'] },
				{ emoji: '🫀', name: 'anatomical heart', keywords: ['heart', 'cardio'] },
				{ emoji: '🫁', name: 'lungs', keywords: ['breathe', 'respiratory'] },
				{ emoji: '🦷', name: 'tooth', keywords: ['dental', 'dentist'] },
				{ emoji: '🦴', name: 'bone', keywords: ['skeleton', 'orthopedic'] },
				{ emoji: '👁️', name: 'eye', keywords: ['vision', 'optometrist'] },
				{ emoji: '🛌', name: 'person in bed', keywords: ['sleep', 'rest'] },
				{ emoji: '🍎', name: 'red apple', keywords: ['fruit', 'healthy'] },
				{ emoji: '🥗', name: 'green salad', keywords: ['healthy', 'diet'] },
				{ emoji: '💧', name: 'droplet', keywords: ['water', 'hydrate'] },
				{ emoji: '🧊', name: 'ice', keywords: ['cold therapy', 'recover'] }
			]
		},
		{
			category: 'Learning & Science',
			values: [
				{ emoji: '📚', name: 'books', keywords: ['study', 'read', 'learn'] },
				{ emoji: '📖', name: 'open book', keywords: ['read', 'research'] },
				{ emoji: '📕', name: 'closed book', keywords: ['red', 'textbook'] },
				{ emoji: '📗', name: 'green book', keywords: ['textbook', 'study'] },
				{ emoji: '📘', name: 'blue book', keywords: ['textbook', 'class'] },
				{ emoji: '📙', name: 'orange book', keywords: ['textbook', 'manual'] },
				{ emoji: '📓', name: 'notebook', keywords: ['journal', 'notes'] },
				{ emoji: '📒', name: 'ledger', keywords: ['accounting', 'record'] },
				{ emoji: '📔', name: 'notebook decorative', keywords: ['diary', 'journal'] },
				{ emoji: '🎓', name: 'graduation cap', keywords: ['education', 'degree'] },
				{ emoji: '🏫', name: 'school', keywords: ['education', 'class'] },
				{ emoji: '🔬', name: 'microscope', keywords: ['science', 'biology'] },
				{ emoji: '🔭', name: 'telescope', keywords: ['astronomy', 'space'] },
				{ emoji: '🧪', name: 'test tube', keywords: ['chemistry', 'experiment'] },
				{ emoji: '🧫', name: 'petri dish', keywords: ['biology', 'culture'] },
				{ emoji: '🧮', name: 'abacus', keywords: ['math', 'calculate'] },
				{ emoji: '🧬', name: 'dna', keywords: ['genetics', 'biology'] },
				{ emoji: '🌍', name: 'globe europe africa', keywords: ['earth', 'world'] },
				{ emoji: '🌎', name: 'globe americas', keywords: ['earth', 'world'] },
				{ emoji: '🌏', name: 'globe asia australia', keywords: ['earth', 'world'] },
				{ emoji: '🪐', name: 'ringed planet', keywords: ['saturn', 'space'] },
				{ emoji: '🌌', name: 'milky way', keywords: ['galaxy', 'space'] },
				{ emoji: '⚛️', name: 'atom symbol', keywords: ['science', 'physics'] },
				{ emoji: '🧠', name: 'brain', keywords: ['think', 'mind', 'smart'] },
				{ emoji: '💬', name: 'speech balloon', keywords: ['talk', 'chat'] },
				{ emoji: '💭', name: 'thought balloon', keywords: ['think', 'idea'] },
				{ emoji: '📰', name: 'newspaper', keywords: ['news', 'article'] },
				{ emoji: '🗞️', name: 'rolled-up newspaper', keywords: ['press', 'media'] }
			]
		},
		{
			category: 'Hearts & Symbols',
			values: [
				{ emoji: '❤️', name: 'red heart', keywords: ['love', 'like'] },
				{ emoji: '🧡', name: 'orange heart', keywords: ['love', 'warm'] },
				{ emoji: '💛', name: 'yellow heart', keywords: ['love', 'friendship'] },
				{ emoji: '💚', name: 'green heart', keywords: ['love', 'nature'] },
				{ emoji: '💙', name: 'blue heart', keywords: ['love', 'trust'] },
				{ emoji: '💜', name: 'purple heart', keywords: ['love', 'royal'] },
				{ emoji: '🖤', name: 'black heart', keywords: ['dark', 'goth'] },
				{ emoji: '🤍', name: 'white heart', keywords: ['pure', 'clean'] },
				{ emoji: '🤎', name: 'brown heart', keywords: ['earth', 'warm'] },
				{ emoji: '💔', name: 'broken heart', keywords: ['sad', 'breakup'] },
				{ emoji: '❣️', name: 'heart exclamation', keywords: ['love', 'emphasis'] },
				{ emoji: '💕', name: 'two hearts', keywords: ['love', 'couple'] },
				{ emoji: '💞', name: 'revolving hearts', keywords: ['love', 'affection'] },
				{ emoji: '💓', name: 'beating heart', keywords: ['love', 'alive'] },
				{ emoji: '💗', name: 'growing heart', keywords: ['love', 'expand'] },
				{ emoji: '💖', name: 'sparkling heart', keywords: ['love', 'special'] },
				{ emoji: '💘', name: 'heart with arrow', keywords: ['cupid', 'love'] },
				{ emoji: '🫶', name: 'heart hands', keywords: ['love', 'adore'] },
				{ emoji: '⭐', name: 'star', keywords: ['favorite', 'rating'] },
				{ emoji: '🌟', name: 'glowing star', keywords: ['sparkle', 'bright'] },
				{ emoji: '✨', name: 'sparkles', keywords: ['magic', 'new', 'clean'] },
				{ emoji: '💫', name: 'dizzy', keywords: ['star', 'shooting'] },
				{ emoji: '🔥', name: 'fire', keywords: ['hot', 'lit', 'trending'] },
				{ emoji: '⚡', name: 'high voltage', keywords: ['lightning', 'power'] },
				{ emoji: '💥', name: 'collision', keywords: ['boom', 'explosion'] },
				{ emoji: '💢', name: 'anger symbol', keywords: ['angry', 'mad'] },
				{ emoji: '💤', name: 'zzz', keywords: ['sleep', 'tired'] },
				{ emoji: '🕳️', name: 'hole', keywords: ['pit', 'empty'] },
				{ emoji: '💣', name: 'bomb', keywords: ['explosive', 'danger'] },
				{ emoji: '🎉', name: 'party popper', keywords: ['celebrate', 'congratulations'] },
				{ emoji: '🎊', name: 'confetti ball', keywords: ['party', 'celebrate'] },
				{ emoji: '🎈', name: 'balloon', keywords: ['party', 'birthday'] },
				{ emoji: '🎀', name: 'ribbon', keywords: ['bow', 'gift'] },
				{ emoji: '🎁', name: 'wrapped gift', keywords: ['present', 'birthday'] },
				{ emoji: '🏳️', name: 'white flag', keywords: ['surrender', 'peace'] },
				{ emoji: '🏴', name: 'black flag', keywords: ['pirate', 'flag'] },
				{ emoji: '🚩', name: 'triangular flag', keywords: ['red flag', 'warning'] },
				{ emoji: '🏁', name: 'chequered flag', keywords: ['finish', 'race'] }
			]
		},
		{
			category: 'Signs & Arrows',
			values: [
				{ emoji: '✅', name: 'check mark', keywords: ['done', 'yes', 'correct'] },
				{ emoji: '❌', name: 'cross mark', keywords: ['no', 'wrong', 'delete'] },
				{ emoji: '❓', name: 'question mark', keywords: ['ask', 'help'] },
				{ emoji: '❗', name: 'exclamation mark', keywords: ['important', 'alert'] },
				{ emoji: '‼️', name: 'double exclamation', keywords: ['urgent', 'important'] },
				{ emoji: '⁉️', name: 'exclamation question', keywords: ['surprise', 'wtf'] },
				{ emoji: '⚠️', name: 'warning', keywords: ['caution', 'alert'] },
				{ emoji: '🚫', name: 'prohibited', keywords: ['no', 'forbidden'] },
				{ emoji: '🔞', name: 'no one under eighteen', keywords: ['adult', 'age'] },
				{ emoji: '⛔', name: 'no entry', keywords: ['stop', 'forbidden'] },
				{ emoji: '🛑', name: 'stop sign', keywords: ['stop', 'halt'] },
				{ emoji: '🔴', name: 'red circle', keywords: ['dot', 'stop'] },
				{ emoji: '🟠', name: 'orange circle', keywords: ['dot', 'medium'] },
				{ emoji: '🟡', name: 'yellow circle', keywords: ['dot', 'caution'] },
				{ emoji: '🟢', name: 'green circle', keywords: ['dot', 'go'] },
				{ emoji: '🔵', name: 'blue circle', keywords: ['dot', 'info'] },
				{ emoji: '🟣', name: 'purple circle', keywords: ['dot', 'special'] },
				{ emoji: '⚫', name: 'black circle', keywords: ['dot', 'dark'] },
				{ emoji: '⚪', name: 'white circle', keywords: ['dot', 'empty'] },
				{ emoji: '🟥', name: 'red square', keywords: ['block', 'stop'] },
				{ emoji: '🟧', name: 'orange square', keywords: ['block'] },
				{ emoji: '🟨', name: 'yellow square', keywords: ['block'] },
				{ emoji: '🟩', name: 'green square', keywords: ['block', 'go'] },
				{ emoji: '🟦', name: 'blue square', keywords: ['block'] },
				{ emoji: '🟪', name: 'purple square', keywords: ['block'] },
				{ emoji: '⬛', name: 'black square', keywords: ['block', 'dark'] },
				{ emoji: '⬜', name: 'white square', keywords: ['block', 'empty'] },
				{ emoji: '🔶', name: 'large orange diamond', keywords: ['shape'] },
				{ emoji: '🔷', name: 'large blue diamond', keywords: ['shape'] },
				{ emoji: '🔺', name: 'red triangle up', keywords: ['shape', 'increase'] },
				{ emoji: '🔻', name: 'red triangle down', keywords: ['shape', 'decrease'] },
				{ emoji: '♻️', name: 'recycling', keywords: ['recycle', 'green'] },
				{ emoji: '♾️', name: 'infinity', keywords: ['forever', 'unlimited'] },
				{ emoji: '🆕', name: 'new', keywords: ['fresh', 'latest'] },
				{ emoji: '🆗', name: 'ok', keywords: ['okay', 'approve'] },
				{ emoji: '🆙', name: 'up', keywords: ['upgrade', 'level up'] },
				{ emoji: '🔜', name: 'soon', keywords: ['coming', 'next'] },
				{ emoji: '🔝', name: 'top', keywords: ['best', 'first'] },
				{ emoji: '🔄', name: 'counterclockwise arrows', keywords: ['refresh', 'reload'] },
				{ emoji: '🔃', name: 'clockwise arrows', keywords: ['cycle', 'repeat'] },
				{ emoji: '➡️', name: 'right arrow', keywords: ['next', 'forward'] },
				{ emoji: '⬅️', name: 'left arrow', keywords: ['back', 'previous'] },
				{ emoji: '⬆️', name: 'up arrow', keywords: ['above', 'increase'] },
				{ emoji: '⬇️', name: 'down arrow', keywords: ['below', 'decrease'] },
				{ emoji: '↗️', name: 'up-right arrow', keywords: ['growth', 'increase'] },
				{ emoji: '↘️', name: 'down-right arrow', keywords: ['decline'] },
				{ emoji: '🔙', name: 'back', keywords: ['return', 'previous'] },
				{ emoji: '🔚', name: 'end', keywords: ['finish', 'complete'] },
				{ emoji: '🔛', name: 'on', keywords: ['switch', 'active'] }
			]
		},
		{
			category: 'Numbers & Letters',
			values: [
				{ emoji: '0️⃣', name: 'keycap 0', keywords: ['zero', 'number'] },
				{ emoji: '1️⃣', name: 'keycap 1', keywords: ['one', 'first'] },
				{ emoji: '2️⃣', name: 'keycap 2', keywords: ['two', 'second'] },
				{ emoji: '3️⃣', name: 'keycap 3', keywords: ['three', 'third'] },
				{ emoji: '4️⃣', name: 'keycap 4', keywords: ['four', 'fourth'] },
				{ emoji: '5️⃣', name: 'keycap 5', keywords: ['five', 'fifth'] },
				{ emoji: '6️⃣', name: 'keycap 6', keywords: ['six', 'sixth'] },
				{ emoji: '7️⃣', name: 'keycap 7', keywords: ['seven', 'seventh'] },
				{ emoji: '8️⃣', name: 'keycap 8', keywords: ['eight', 'eighth'] },
				{ emoji: '9️⃣', name: 'keycap 9', keywords: ['nine', 'ninth'] },
				{ emoji: '🔟', name: 'keycap 10', keywords: ['ten', 'tenth'] },
				{ emoji: '#️⃣', name: 'keycap hash', keywords: ['number', 'pound'] },
				{ emoji: '*️⃣', name: 'keycap star', keywords: ['asterisk'] },
				{ emoji: '🅰️', name: 'a button', keywords: ['letter', 'grade'] },
				{ emoji: '🅱️', name: 'b button', keywords: ['letter', 'grade'] },
				{ emoji: '🆎', name: 'ab button', keywords: ['blood type'] },
				{ emoji: '🅾️', name: 'o button', keywords: ['letter', 'blood type'] },
				{ emoji: 'ℹ️', name: 'information', keywords: ['info', 'help'] },
				{ emoji: '🅿️', name: 'p button', keywords: ['parking', 'letter'] },
				{ emoji: 'Ⓜ️', name: 'm circled', keywords: ['metro', 'letter'] },
				{ emoji: '🔠', name: 'input latin uppercase', keywords: ['abc', 'letters'] },
				{ emoji: '🔡', name: 'input latin lowercase', keywords: ['abc', 'letters'] },
				{ emoji: '🔢', name: 'input numbers', keywords: ['123', 'digits'] },
				{ emoji: '🔣', name: 'input symbols', keywords: ['characters', 'special'] },
				{ emoji: '🔤', name: 'input latin letters', keywords: ['abc', 'alphabet'] },
				{ emoji: '🆓', name: 'free', keywords: ['gratis', 'no cost'] },
				{ emoji: '🆔', name: 'id', keywords: ['identity', 'badge'] },
				{ emoji: '🆘', name: 'sos', keywords: ['help', 'emergency'] },
				{ emoji: '🆚', name: 'vs', keywords: ['versus', 'against'] },
				{ emoji: '🈲', name: 'prohibited', keywords: ['japanese', 'no'] },
				{ emoji: '🈳', name: 'vacancy', keywords: ['japanese', 'empty'] },
				{ emoji: '©️', name: 'copyright', keywords: ['legal', 'rights'] },
				{ emoji: '®️', name: 'registered', keywords: ['trademark'] },
				{ emoji: '™️', name: 'trade mark', keywords: ['brand', 'tm'] }
			]
		},
		{
			category: 'Flags',
			values: [
				{ emoji: '🏳️', name: 'white flag', keywords: ['surrender', 'peace'] },
				{ emoji: '🏴', name: 'black flag', keywords: ['pirate'] },
				{ emoji: '🏁', name: 'chequered flag', keywords: ['finish', 'race'] },
				{ emoji: '🚩', name: 'triangular flag', keywords: ['red flag', 'warning'] },
				{ emoji: '🏳️‍🌈', name: 'rainbow flag', keywords: ['pride', 'lgbtq'] },
				{ emoji: '🏳️‍⚧️', name: 'transgender flag', keywords: ['trans', 'pride'] },
				{ emoji: '🏴‍☠️', name: 'pirate flag', keywords: ['pirate', 'jolly roger'] },
				{ emoji: '🇺🇸', name: 'flag usa', keywords: ['united states', 'america'] },
				{ emoji: '🇬🇧', name: 'flag uk', keywords: ['united kingdom', 'britain'] },
				{ emoji: '🇫🇷', name: 'flag france', keywords: ['french'] },
				{ emoji: '🇩🇪', name: 'flag germany', keywords: ['german'] },
				{ emoji: '🇮🇹', name: 'flag italy', keywords: ['italian'] },
				{ emoji: '🇪🇸', name: 'flag spain', keywords: ['spanish'] },
				{ emoji: '🇯🇵', name: 'flag japan', keywords: ['japanese'] },
				{ emoji: '🇰🇷', name: 'flag south korea', keywords: ['korean'] },
				{ emoji: '🇨🇳', name: 'flag china', keywords: ['chinese'] },
				{ emoji: '🇮🇳', name: 'flag india', keywords: ['indian'] },
				{ emoji: '🇧🇷', name: 'flag brazil', keywords: ['brazilian'] },
				{ emoji: '🇲🇽', name: 'flag mexico', keywords: ['mexican'] },
				{ emoji: '🇨🇦', name: 'flag canada', keywords: ['canadian'] },
				{ emoji: '🇦🇺', name: 'flag australia', keywords: ['australian'] },
				{ emoji: '🇷🇺', name: 'flag russia', keywords: ['russian'] },
				{ emoji: '🇿🇦', name: 'flag south africa', keywords: ['south african'] },
				{ emoji: '🇳🇬', name: 'flag nigeria', keywords: ['nigerian'] },
				{ emoji: '🇪🇬', name: 'flag egypt', keywords: ['egyptian'] },
				{ emoji: '🇰🇪', name: 'flag kenya', keywords: ['kenyan'] },
				{ emoji: '🇸🇪', name: 'flag sweden', keywords: ['swedish'] },
				{ emoji: '🇳🇴', name: 'flag norway', keywords: ['norwegian'] },
				{ emoji: '🇵🇱', name: 'flag poland', keywords: ['polish'] },
				{ emoji: '🇹🇷', name: 'flag turkey', keywords: ['turkish'] },
				{ emoji: '🇸🇦', name: 'flag saudi arabia', keywords: ['saudi'] },
				{ emoji: '🇦🇪', name: 'flag uae', keywords: ['emirates', 'dubai'] },
				{ emoji: '🇮🇱', name: 'flag israel', keywords: ['israeli'] },
				{ emoji: '🇹🇭', name: 'flag thailand', keywords: ['thai'] },
				{ emoji: '🇻🇳', name: 'flag vietnam', keywords: ['vietnamese'] },
				{ emoji: '🇵🇭', name: 'flag philippines', keywords: ['filipino'] },
				{ emoji: '🇮🇩', name: 'flag indonesia', keywords: ['indonesian'] },
				{ emoji: '🇦🇷', name: 'flag argentina', keywords: ['argentinian'] },
				{ emoji: '🇨🇴', name: 'flag colombia', keywords: ['colombian'] },
				{ emoji: '🇨🇭', name: 'flag switzerland', keywords: ['swiss'] },
				{ emoji: '🇳🇱', name: 'flag netherlands', keywords: ['dutch'] },
				{ emoji: '🇵🇹', name: 'flag portugal', keywords: ['portuguese'] },
				{ emoji: '🇬🇷', name: 'flag greece', keywords: ['greek'] },
				{ emoji: '🇮🇪', name: 'flag ireland', keywords: ['irish'] },
				{ emoji: '🇳🇿', name: 'flag new zealand', keywords: ['kiwi'] }
			]
		},
		{
			category: 'Clothing & Accessories',
			values: [
				{ emoji: '👓', name: 'glasses', keywords: ['eyeglasses', 'read'] },
				{ emoji: '🕶️', name: 'sunglasses', keywords: ['cool', 'shades'] },
				{ emoji: '🥽', name: 'goggles', keywords: ['safety', 'swim'] },
				{ emoji: '👔', name: 'necktie', keywords: ['formal', 'business'] },
				{ emoji: '👕', name: 't-shirt', keywords: ['casual', 'shirt'] },
				{ emoji: '👖', name: 'jeans', keywords: ['pants', 'denim'] },
				{ emoji: '🧣', name: 'scarf', keywords: ['winter', 'warm'] },
				{ emoji: '🧤', name: 'gloves', keywords: ['winter', 'cold'] },
				{ emoji: '🧥', name: 'coat', keywords: ['jacket', 'winter'] },
				{ emoji: '🧦', name: 'socks', keywords: ['feet', 'warm'] },
				{ emoji: '👗', name: 'dress', keywords: ['fashion', 'formal'] },
				{ emoji: '👘', name: 'kimono', keywords: ['japanese', 'traditional'] },
				{ emoji: '🥻', name: 'sari', keywords: ['indian', 'traditional'] },
				{ emoji: '👙', name: 'bikini', keywords: ['swimsuit', 'beach'] },
				{ emoji: '👚', name: 'womans clothes', keywords: ['blouse', 'shirt'] },
				{ emoji: '👛', name: 'purse', keywords: ['wallet', 'bag'] },
				{ emoji: '👜', name: 'handbag', keywords: ['bag', 'purse'] },
				{ emoji: '🎒', name: 'backpack', keywords: ['school', 'bag'] },
				{ emoji: '👞', name: 'mans shoe', keywords: ['formal', 'oxford'] },
				{ emoji: '👟', name: 'running shoe', keywords: ['sneaker', 'athletic'] },
				{ emoji: '🥾', name: 'hiking boot', keywords: ['outdoor', 'hike'] },
				{ emoji: '👠', name: 'high-heeled shoe', keywords: ['heel', 'formal'] },
				{ emoji: '👡', name: 'womans sandal', keywords: ['sandal', 'summer'] },
				{ emoji: '👑', name: 'crown', keywords: ['king', 'queen', 'royal'] },
				{ emoji: '🎩', name: 'top hat', keywords: ['formal', 'gentleman'] },
				{ emoji: '🧢', name: 'billed cap', keywords: ['baseball', 'hat'] },
				{ emoji: '⛑️', name: 'rescue workers helmet', keywords: ['safety', 'hard hat'] },
				{ emoji: '💍', name: 'ring', keywords: ['engagement', 'wedding'] },
				{ emoji: '💄', name: 'lipstick', keywords: ['makeup', 'cosmetics'] },
				{ emoji: '👝', name: 'clutch bag', keywords: ['evening', 'purse'] },
				{ emoji: '🎀', name: 'ribbon', keywords: ['bow', 'hair'] },
				{ emoji: '📿', name: 'prayer beads', keywords: ['necklace', 'spiritual'] }
			]
		},
		{
			category: 'Miscellaneous',
			values: [
				{ emoji: '🎉', name: 'party popper', keywords: ['celebrate', 'congratulations'] },
				{ emoji: '🎊', name: 'confetti ball', keywords: ['party', 'celebrate'] },
				{ emoji: '🎈', name: 'balloon', keywords: ['party', 'birthday'] },
				{ emoji: '🎁', name: 'wrapped gift', keywords: ['present', 'gift'] },
				{ emoji: '🎗️', name: 'reminder ribbon', keywords: ['awareness', 'cause'] },
				{ emoji: '🎟️', name: 'admission tickets', keywords: ['event', 'show'] },
				{ emoji: '🎫', name: 'ticket', keywords: ['admission', 'pass'] },
				{ emoji: '🔮', name: 'crystal ball', keywords: ['fortune', 'predict'] },
				{ emoji: '🪄', name: 'magic wand', keywords: ['spell', 'wizard'] },
				{ emoji: '🎭', name: 'performing arts', keywords: ['theater', 'drama'] },
				{ emoji: '🎪', name: 'circus tent', keywords: ['show', 'carnival'] },
				{ emoji: '🛒', name: 'shopping cart', keywords: ['buy', 'store'] },
				{ emoji: '🚧', name: 'construction', keywords: ['wip', 'in progress'] },
				{ emoji: '⚓', name: 'anchor', keywords: ['ship', 'harbor'] },
				{ emoji: '🪝', name: 'hook', keywords: ['fishing', 'hang'] },
				{ emoji: '⛓️', name: 'chains', keywords: ['linked', 'locked'] },
				{ emoji: '🧿', name: 'nazar amulet', keywords: ['evil eye', 'protection'] },
				{ emoji: '🪬', name: 'hamsa', keywords: ['protection', 'luck'] },
				{ emoji: '♨️', name: 'hot springs', keywords: ['onsen', 'steam'] },
				{ emoji: '🗻', name: 'mount fuji', keywords: ['japan', 'mountain'] },
				{ emoji: '🌐', name: 'globe with meridians', keywords: ['internet', 'web', 'world'] },
				{ emoji: '🛡️', name: 'shield', keywords: ['protect', 'defense'] },
				{ emoji: '⚔️', name: 'crossed swords', keywords: ['battle', 'fight'] },
				{ emoji: '🏹', name: 'bow and arrow', keywords: ['archery', 'aim'] },
				{ emoji: '🪃', name: 'boomerang', keywords: ['return', 'throw'] },
				{ emoji: '🩴', name: 'thong sandal', keywords: ['flip flop', 'beach'] },
				{ emoji: '🪩', name: 'mirror ball', keywords: ['disco', 'party'] },
				{ emoji: '🫧', name: 'bubbles', keywords: ['soap', 'clean'] },
				{ emoji: '🪆', name: 'nesting dolls', keywords: ['matryoshka', 'russian'] },
				{ emoji: '🧸', name: 'teddy bear', keywords: ['stuffed', 'toy', 'cute'] },
				{ emoji: '🪁', name: 'kite', keywords: ['fly', 'wind'] },
				{ emoji: '🎐', name: 'wind chime', keywords: ['bell', 'japanese'] }
			]
		}
	];

	let {
		open = false,
		onClose = () => {},
		onSelect = (_emoji: string) => {}
	}: {
		open?: boolean;
		onClose?: () => void;
		onSelect?: (emoji: string) => void;
	} = $props();

	let query = $state('');
	const normalizedQuery = $derived(query.trim().toLowerCase());

	const filtered = $derived(
		EMOJIS.map((group) => ({
			...group,
			values: group.values.filter((item) => {
				if (!normalizedQuery) return true;
				const haystack = `${group.category} ${item.name} ${item.keywords.join(' ')}`.toLowerCase();
				return haystack.includes(normalizedQuery) || item.emoji.includes(normalizedQuery);
			})
		})).filter((group) => group.values.length > 0)
	);

	function handleSelect(emoji: string): void {
		onSelect(emoji);
		onClose();
	}

	function handleBackdrop(event: MouseEvent): void {
		if (event.target === event.currentTarget) {
			onClose();
		}
	}

	function handleKey(event: KeyboardEvent): void {
		if (event.key === 'Escape') {
			onClose();
		}
	}
</script>

{#if open}
	<div class="backdrop" onclick={handleBackdrop} onkeydown={handleKey} tabindex="0" role="dialog" aria-modal="true">
		<div class="picker">
			<input bind:value={query} placeholder="Search emoji..." />
			{#each filtered as group}
				<div class="group">
					<strong>{group.category}</strong>
					<div class="grid">
						{#each group.values as item (`${group.category}-${item.emoji}-${item.name}`)}
							<button
								type="button"
								title={item.name}
								aria-label={item.name}
								data-emoji={item.emoji}
								onclick={() => handleSelect(item.emoji)}
							>
								{item.emoji}
							</button>
						{/each}
					</div>
				</div>
			{/each}
			{#if filtered.length === 0}
				<p class="empty">No emoji found for "{query}".</p>
			{/if}
		</div>
	</div>
{/if}

<style>
	.backdrop {
		position: fixed;
		inset: 0;
		background: var(--backdrop);
		backdrop-filter: blur(2px);
		display: grid;
		place-items: center;
		z-index: 50;
	}

	.picker {
		background: var(--bg-surface);
		border-radius: var(--radius-xl);
		padding: 1rem;
		width: min(92vw, 480px);
		max-height: 75vh;
		overflow: auto;
		border: 1px solid var(--border);
		box-shadow: var(--shadow-lg);
	}

	.picker strong {
		font-family: var(--font-display);
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	input {
		width: 100%;
		padding: 0.5rem 0.7rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		margin-bottom: 0.75rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
	}

	input::placeholder {
		color: var(--text-tertiary);
	}

	input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.group {
		margin-bottom: 0.75rem;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(8, minmax(0, 1fr));
		gap: 0.35rem;
		margin-top: 0.35rem;
	}

	button {
		border: 1px solid var(--border-light);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.45rem 0;
		font-size: 1.1rem;
		cursor: pointer;
		transition: all var(--transition);
	}

	button:hover {
		background: var(--accent-light);
		border-color: var(--accent);
		transform: scale(1.1);
	}

	.empty {
		margin: 0.6rem 0 0;
		color: var(--text-secondary);
		font-size: 0.85rem;
	}
</style>
