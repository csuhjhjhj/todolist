<template>
  <div class="layui-container">
    <h1 class="h1-todo">Todo List</h1>
    <div class="todo-inputs">
      <input class="layui-input"
             v-model="newTodo.title"
             placeholder="标题" />
      <input class="layui-input"
             v-model="newTodo.description"
             placeholder="详细描述" />
      <input class="layui-input"
             type="date"
             v-model="newTodo.due_date"
             style="padding-right: 25px; /* 留出空间 */" />
      <!-- <button class="layui-btn"
              @click="addTodo">Add Todo</button> -->
      <button class="layui-btn add-todo-button"
              @click="addTodo">Add Todo</button>
    </div>
    <div class="todo-list">
      <div class="todo-item"
           v-for="todo in todos"
           :key="todo.id">
        <div class="content">
          <div class="title">{{ todo.title }}</div>
          <div class="description">{{ todo.description }}</div>
          <div class="date">截止日期: {{ formatDate(todo.due_date) }}</div>
        </div>
        <div class="actions">
          <button @click="toggleCompletion(todo)"
                  :class="{'completed-icon': todo.completed, 'not-completed-icon': !todo.completed}">
            <i class="layui-icon"
               v-if="todo.completed">✅</i>
            <i class="layui-icon"
               v-else>◯</i>
          </button>
          <button @click="deleteTodo(todo.id)">
            <i class="layui-icon layui-icon-delete "></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  data () {
    return {
      todos: [],
      newTodo: {
        title: '',
        description: '',
        due_date: '',
        completed: false
      }
    };
  },
  created () {
    this.fetchTodos();
  },
  methods: {
    formatDate (value) {
      return new Date(value).toLocaleDateString();
    },
    fetchTodos () {
      axios.get('http://localhost:5001/api/todos').then(response => {
        this.todos = response.data;
        this.sortTodos(); // 排序函数调用
      }).catch(error => {
        console.error('Error fetching todos:', error);
      });
    },
    addTodo () {
      console.log("Adding a new todo item");
      if (!this.newTodo.title || !this.newTodo.description || !this.newTodo.due_date) {
        alert('All fields must be filled!');
        return;
      }
      axios.post('http://localhost:5001/api/todos', this.newTodo).then(response => {
        this.todos.push(response.data);
        this.newTodo = { title: '', description: '', due_date: '', completed: false };
        alert('Todo added successfully!');
      }).catch(error => {
        console.error('Error adding todo:', error);
        alert('Failed to add todo.');
      });
    },
    sortTodos () {
      // 按完成状态排序，未完成的在前，完成的在后
      this.todos.sort((a, b) => a.completed - b.completed);
    },
    toggleCompletion (todo) {
      const updatedTodos = this.todos.map(t =>
        t.id === todo.id ? { ...t, completed: !t.completed } : t
      );

      axios.put(`http://localhost:5001/api/todos/${todo.id}`, {
        ...todo,
        completed: !todo.completed
      })
        .then(() => {
          this.todos = updatedTodos;  // 直接替换整个数组
          this.sortTodos();
        })
        .catch(error => {
          console.error("Error updating todo:", error);
        });
    }

    ,
    deleteTodo (id) {
      axios.delete(`http://localhost:5001/api/todos/${id}`).then(() => {
        this.todos = this.todos.filter(t => t.id !== id);
      }).catch(error => {
        console.error('Error deleting todo:', error);
      });
    }
  }
}
</script>


<style scoped>
/* 居中并美化标题 */
.h1-todo {
  text-align: center; /* 文本居中 */
  font-size: 24px; /* 增大字体大小 */
  color: #4a90e2; /* 设定特定颜色 */
  margin-top: 20px; /* 上边距 */
  margin-bottom: 20px; /* 下边距 */
  font-weight: bold; /* 字体加粗 */
}

/* 全局字体和背景 */
.layui-container {
  font-family: 'Arial', sans-serif;
  background-color: #f7f7f7;
  color: #333;
}

/* 输入部分样式 */
.todo-inputs {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.input {
  margin-bottom: 10px;
  width: 100%;
}

/* 待办事项列表样式 */
.todo-list {
  display: flex;
  flex-direction: column;
}

/* 单个待办事项样式 */
.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #eee; /* 添加底部边界以区分各待办事项 */
  margin-bottom: 10px; /* 每个项目之间的间隔 */
}

.todo-item:hover {
  background-color: #eef;
}

/* 内容区样式 */
.content {
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.title {
  font-weight: bold;
  font-size: 18px; /* 标题字体大小 */
  color: #333; /* 标题颜色 */
}
.description {
  font-size: 16px; /* 描述字体大小 */
  color: #666; /* 描述文字颜色 */
  margin-left: 20px; /* 与标题的间隔 */
}
.date {
  font-size: 14px; /* 日期字体大小 */
  color: #999; /* 日期文字颜色 */
  margin-left: auto; /* 自动左边距，推送到右边 */
}

.title {
  font-weight: bold;
  font-size: 20px;
}

.description {
  font-size: 16px;
  color: #666;
}

.date {
  font-size: 14px;
  color: #999;
  margin-left: auto;
}

/* 动作按钮样式 */
.actions button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px 10px;
}

button:focus {
  outline: none;
}

.completed-icon,
.not-completed-icon {
  font-size: 24px;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .title {
    font-size: 18px;
  }

  .description,
  .date {
    font-size: 14px;
  }
}
.date i.layui-icon {
  font-size: 20px; /* 调整图标大小 */
  vertical-align: middle; /* 确保图标垂直居中 */
  margin-right: 5px; /* 在图标和文本之间添加一些间隔 */
}
.layui-input[type='date'] {
  font-size: 16px; /* 增大字体大小，这也会影响输入框的高度 */
  padding: 10px; /* 增加内边距，使输入更加舒适 */
  height: auto; /* 设置高度为自动，依据内容调整 */
  width: 100%; /* 全宽，或根据需要调整 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果提高视觉效果 */
}
@media (max-width: 600px) {
  .layui-input[type='date'] {
    font-size: 14px; /* 在较小屏幕上使用更小的字体大小 */
    padding: 8px; /* 在较小屏幕上减少内边距 */
  }
}
/* 美化并居中按钮 */
.add-todo-button {
  display: block; /* 块级元素，允许使用宽度和居中 */
  width: 50%; /* 按钮宽度 */
  margin: 0 auto; /* 自动外边距实现水平居中 */
  background-color: #4caf50; /* 按钮背景颜色 */
  color: white; /* 文字颜色 */
  border: none; /* 无边框 */
  padding: 10px; /* 内边距 */
  border-radius: 5px; /* 圆角边框 */
  cursor: pointer; /* 指针光标 */
  font-size: 16px; /* 字体大小 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 轻微的阴影效果 */
  transition: background-color 0.3s; /* 背景色变化的过渡效果 */
}

.add-todo-button {
  display: inline-block; /* 允许使用宽度和高度 */
  width: auto; /* 按钮自适应内容宽度 */
  padding: 10px 20px; /* 水平和垂直内边距 */
  line-height: 1.5; /* 调整行高以垂直居中文字 */
  text-align: center; /* 文字水平居中 */
  /* 其他样式保持不变 */
}
</style>
