'use strict';

// handle increase/decrease score button click
{
	document.getElementById('predictionForm').addEventListener('click', event => {
		const btnElement = event.target.closest('button');

		if (btnElement?.classList.contains('js_predictionForm_btn')) return changeScore(btnElement);
	});

	function changeScore(btn) {
		if (btn.classList.contains('js_increment_btn')) {
			const scoreInput = btn.closest('label').querySelector('.js_team_score');
			const scoreIncreaseLimit = parseInt(scoreInput.max);

			if (parseInt(scoreInput.value) < scoreIncreaseLimit) scoreInput.value++;
			return;
		}

		if (btn.classList.contains('js_decrement_btn')) {
			const scoreInput = btn.closest('label').querySelector('.js_team_score');
			const scoreDecreaseLimit = parseInt(scoreInput.min);

			if (parseInt(scoreInput.value) > scoreDecreaseLimit) scoreInput.value--;
		}
	}
}

// 'soccer card components' scroll animation effect
{
	const animateOnScroll = (entries, observer) => {
		entries.forEach(entry => {
			// toggle visibility on scroll
			['scale-100', 'opacity-100'].forEach(effect => entry.target.classList.toggle(effect, entry.isIntersecting));

			// make the effect happen only once
			if (entry.isIntersecting) observer.unobserve(entry.target);
		});
	};
	const observerOptions = {
		root: null,
		rootMargin: '100px',
		threshold: 0,
	};
	const observer = new IntersectionObserver(animateOnScroll, observerOptions);

	// handle scroll animation for each card component
	document.querySelectorAll('.soccer-match-card').forEach(element => observer.observe(element));
}
