// Add community functionality at the end of your existing app.js

const communityInput = document.getElementById('communityInput');
const communityPosts = document.getElementById('communityPosts');
const btnSubmitCommunity = document.getElementById('btnSubmitCommunity');

btnSubmitCommunity.addEventListener('click', () => {
  const text = communityInput.value.trim();
  if (!text) return;
  const post = document.createElement('div');
  post.className = 'community-post';
  post.textContent = text;
  communityPosts.prepend(post);
  communityInput.value = '';
});
