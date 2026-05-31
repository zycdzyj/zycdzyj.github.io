// ❌ 删掉这一行：const { random } = require("gsap");

window.addEventListener('load', function() {
  const loader = document.getElementById('glass-loader');
  const loadingText = document.querySelector('.loading-text');
  
  // 1. 页面资源加载完毕后，稍微延迟一点点
  setTimeout(() => {
    // 2. 将模糊度降为 0，背景逐渐变清晰
    loader.style.backdropFilter = 'blur(0px)';
    loader.style.webkitBackdropFilter = 'blur(0px)';
    
    // 3. 同时让“加载中”文字淡出
    loadingText.style.opacity = '0';
    loadingText.style.transition = 'opacity 0.5s';
  }, 500); 

  // 4. 等模糊度完全变为 0 后，彻底移除遮罩层
  setTimeout(() => {
    loader.style.opacity = '0'; 
    setTimeout(() => {
      loader.style.display = 'none'; 
    }, 800);
  }, 1000); 
});

const textElement = document.getElementById('my-text');

const text = [
  "没有人会记得死的东西，所以要活下去，咬牙切齿的活下去！",
  "如果非要爱什么才能让你有信心活下去的话，不如爱我好了。",
  "所谓同伴，就是要踩在他们尸体上，完成他们没做完的事啊！",
  "很多人都能轻易地说出宽恕二字，只是因为他们并不懂仇恨。",
  "有些事你发狠就能牛逼，大部分事你怀着希望赌上命都没用。",
  "我最恨别人抢走属于我的东西……凡我失去的……我要亲手一件件拿回来！",
  "你找到我的时候，我已经忘了你的样子。等我记起你的样子，你已经死了。",
  "仅以此书献给所有有梦想的衰小孩，如果你知道去哪，全世界都会为你让路。",
  "一个人可以逃避世间的一切魔鬼，但惟有一个是他永远无法摆脱的，那就是懦弱的自己。",
  "有些路你和某人一起走，就长得离谱，你和另外一些人走，就短得让人舍不得迈开脚步。",
  "每个人都会有些理由，可以让你豁出命去。你留着命……就是等待把它豁出去的那一天。",
  "命运这种东西，生来就是要被踏于足下的，如果你还未有力量反抗它，只需怀着勇气等待。",
  "每颗戴上王冠的头颅，都要有被砍下的觉悟！",
  "在我们的世界里，王与王的战斗，最终只能靠刀刀见血！",
  "布加迪威龙是世界上最快量产跑车，可它跑不过时光，也跑不过早已注定的命运。",
  "这个世界很温柔，但它不喜欢我。",
  "你扮小丑扮得太久了，演得太入戏，都忘记自己了。",
  "多少红颜为傻逼，多少傻逼不珍惜。",
  "最孤单的人分两种，一种恨不得全世界都跟他一样倒霉，一种则希望别人能幸福，因为看到幸福的人，他也略略觉得温暖。",
  "如果世界真的不喜欢你，那世界就是我的敌人了。",
  "你装出很不在乎的样子，可是你没有对着镜子，看不到自己脸上那么孤独和不甘心。",
  "Let us across hell and reach to heaven! 让我们穿越最深的地狱，然后直抵天堂！",
  "如果喜欢谁，就满世界去找她，别等她来找你，她可能也在等你……别让她等得对你失望了。",
  "南淮是不是那个南淮都无所谓，可和你偷花跳板打枣子的人，都已经不在了。",
  "人长大了就是要跟世界和解的，然后就会感谢你遇到过的绝大多数人。",
  "比孤独更可悲的事情，就是根本不知道自己很孤独，或者分明很孤独，却把自己都骗得相信自己不孤独。",
  "魔鬼是杀不掉的，魔鬼在我们每个人心里。",
  "在亲人的眼里，大义灭亲是个何等残酷的词啊，世间应该有那么一个人，你可以为他背叛一切，甚至于公理和正义。",
  "没有人愿意被关在笼子里，问题是给你一片无边无际的天空，你是不是真的敢要。",
  "时光是无鞍的野马，奔驰起来像闪电，最好的骑手都无法驾驭。",
  "如果喜欢谁，就满世界去找她，别等她来找你，她可能也在等你。"
];

const randomIndex = Math.floor(Math.random() * text.length);
// ✅ 修正后的随机获取逻辑：使用 gsap.utils.random，并将最大值设为 29
textElement.textContent = text[randomIndex];

function updateClock() {
    const now = new Date();
    
    // 1. 在函数内部获取最新的时间
    const year = now.getFullYear();
    const month = now.getMonth() + 1;    
    const day = now.getDate();
    
    // 2. 获取时间字符串
    const timeString = now.toLocaleTimeString(); 
    
    // 3. 使用反引号 ` ` 包裹，并用 ${} 嵌入变量
    const dateString = `${year}年${month}月${day}日`;
    
    // 4. 更新到页面上
    document.getElementById('time').innerText = timeString;
    document.getElementById('date').innerText = dateString;
}
// 页面加载时立即执行一次，避免 1 秒的延迟空白
    updateClock();
// 开启定时器，每秒（1000毫秒）更新一次
    setInterval(updateClock, 1000);

// 1. 获取页面中的各个元素
const audio = document.getElementById('audio');
const playBtn = document.getElementById('play-btn');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress-bar');
const currentTimeEl = document.querySelector('.current-time');
const totalDurationEl = document.querySelector('.total-duration');
const playIcon = document.querySelector('.play-icon');
const pauseIcon = document.querySelector('.pause-icon');

// 2. 播放与暂停功能
function togglePlay() {
    if (audio.paused) {
        audio.play();
        playIcon.style.display = 'none';  // 隐藏播放图标
        pauseIcon.style.display = 'block'; // 显示暂停图标
    } else {
        audio.pause();
        playIcon.style.display = 'block'; // 显示播放图标
        pauseIcon.style.display = 'none';  // 隐藏暂停图标
    }
}
playBtn.addEventListener('click', togglePlay);

// 3. 格式化时间（将秒数转为 0:00 格式）
function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// 4. 当音频元数据加载完成后，更新总时长
audio.addEventListener('loadedmetadata', () => {
    totalDurationEl.textContent = formatTime(audio.duration);
});

// 5. 实时更新进度条和当前播放时间
audio.addEventListener('timeupdate', () => {
    const current = audio.currentTime;
    const duration = audio.duration;
    // 更新进度条的百分比
    progressBar.value = (current / duration) * 100;
    // 更新当前时间显示
    currentTimeEl.textContent = formatTime(current);
});

// 6. 拖动进度条跳转播放位置
progressBar.addEventListener('input', () => {
    const duration = audio.duration;
    // 根据拖动的百分比计算出目标时间
    audio.currentTime = (progressBar.value / 100) * duration;
});

// 7. 预留上一首、下一首的点击事件（等你有多首歌曲时可以扩展）
prevBtn.addEventListener('click', () => {
    console.log('点击了上一首');
    // 这里可以写切换上一首歌曲的逻辑
});

nextBtn.addEventListener('click', () => {
    console.log('点击了下一首');
    // 这里可以写切换下一首歌曲的逻辑
});