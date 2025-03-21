<template>
    <div class="lottery-container">
      <!-- 头部导航 -->
      <header class="header">
        <nav>
          <ul class="nav-list">
            <li v-for="(item, index) in navItems" :key="index" :class="{ active: item.active }" @click="toggleNav(item)">
              {{ item.name }}
            </li>
          </ul>
        </nav>
      </header>

      <section class="latest-result">
        <h3>{{ latestIssue || '--' }}期最新开奖</h3>
        <p>{{ openDate || '加载中...' }}</p>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-else class="result-numbers">
          <span v-for="number in latestNumbers" :key="number">{{ number }}</span>
        </div>
        <p>奖池: {{ prizePool || '0.00' }}亿 每日21:30开奖</p>
      </section>
    </div>
  </template>
  

  <script>
  export default {
    name: 'LotteryView',
    data() {
      return {
        navItems: [
          { name: '快乐8', active: true },
          { name: '排列5', active: false },
          // 其他导航项...
        ],
        latestNumbers: [],
        latestIssue: '',
        openDate: '',
        prizePool: '0.00', // 初始化默认值
        loading: false,
        error: null
      };
    },
    created() {
      this.fetchLatestNumbers(); // 添加生命周期钩子
    },
    methods: {
      toggleNav(item) {
        this.navItems.forEach(nav => (nav.active = false));
        item.active = true;
      },
      navigateTo(route) {
        console.log(`Navigating to ${route}`);
        // 实现路由跳转逻辑
      },
      async fetchLatestNumbers() {
        try {
          this.loading = true; // 确保loading状态被更新
          const response = await fetch('http://localhost:8000/api/kl8/?limit=5');
          
          // 添加网络错误检查
          if (!response.ok) {
            throw new Error(`HTTP错误! 状态码: ${response.status}`);
          }
          
          // 添加空响应检查
          const responseText = await response.text();
          if (!responseText) {
            throw new Error('服务器返回空响应');
          }

          const { status, data } = JSON.parse(responseText);
          
          // 确保这里使用 status 进行验证
          if (status !== 'success') {
            throw new Error(`API状态异常: ${status}`);
          }
          
          // 添加数据有效性检查
          if (!data || data.length === 0) {
            throw new Error('没有可用的开奖数据');
          }

          const latest = data[0];
          // 添加字段存在性检查
          if (!latest?.front_winning_num || !latest?.issue) {
            throw new Error('数据字段不完整');
          }

          // 解析数据字段
          this.latestIssue = latest.issue;
          this.openDate = this.formatDate(latest.open_time);
          this.prizePool = latest.prize_pool_money;
          this.latestNumbers = latest.front_winning_num.split(','); // 假设号码用逗号分隔
        } catch (err) {
          this.error = `数据加载失败: ${err.message}`; // 更详细的错误提示
          console.error('完整错误日志:', err);
        } finally {
          this.loading = false;
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
        return `${(date.getMonth() + 1).toString().padStart(2, '0')}月${date.getDate().toString().padStart(2, '0')}日 周${weekdays[date.getDay()]}`;
      }
    }
  };
  </script>

  <style>
  .error-message {
    color: red;
    padding: 10px;
  }
  </style>