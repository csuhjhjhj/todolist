Page({
  data: {
    todos: [],
    newTodo: {
      title: '',
      description: '',
      due_date: '',
      completed: false
    }
  },

  onLoad: function () {
    this.fetchTodos();
  },

  fetchTodos: function () {
    wx.request({
      url: 'http://localhost:5001/api/todos',
      method: 'GET',
      success: (res) => {
        this.setData({
          todos: this.sortTodos(res.data)
        });
      },
      fail: (err) => {
        console.error('Failed to fetch todos', err);
      }
    });
  },

  addTodo: function () {
    const { title, description, due_date } = this.data.newTodo;
    if (!title || !description || !due_date) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      });
      return;
    }

    wx.request({
      url: 'http://localhost:5001/api/todos',
      method: 'POST',
      data: this.data.newTodo,
      success: (res) => {
        const newTodo = res.data;
        this.setData({
          todos: this.sortTodos([...this.data.todos, newTodo]),
          newTodo: { title: '', description: '', due_date: '', completed: false }
        });
        wx.showToast({
          title: '添加成功',
          icon: 'success'
        });
      },
      fail: (err) => {
        console.error('Failed to add todo', err);
        wx.showToast({
          title: '添加失败',
          icon: 'none'
        });
      }
    });
  },

  deleteTodo: function (e) {
    const id = e.currentTarget.dataset.id;
    wx.request({
      url: `http://localhost:5001/api/todos/${id}`,
      method: 'DELETE',
      success: (res) => {
        const updatedTodos = this.data.todos.filter(todo => todo.id !== id);
        this.setData({
          todos: this.sortTodos(updatedTodos)
        });
        wx.showToast({
          title: '删除成功',
          icon: 'success'
        });
      },
      fail: (err) => {
        console.error('Failed to delete todo', err);
        wx.showToast({
          title: '删除失败',
          icon: 'none'
        });
      }
    });
  },

  toggleCompletion: function (e) {
    const id = e.currentTarget.dataset.id;
    const todo = this.data.todos.find(todo => todo.id === id);
    if (!todo) return;

    wx.request({
      url: `http://localhost:5001/api/todos/${id}`,
      method: 'PUT',
      data: {
        ...todo,
        completed: !todo.completed
      },
      success: (res) => {
        const updatedTodos = this.data.todos.map(t =>
          t.id === id ? { ...t, completed: !t.completed } : t
        );
        this.setData({
          todos: this.sortTodos(updatedTodos)
        });
        wx.showToast({
          title: '更新成功',
          icon: 'success'
        });
      },
      fail: (err) => {
        console.error('Failed to update todo', err);
        wx.showToast({
          title: '更新失败',
          icon: 'none'
        });
      }
    });
  },

  bindTitleInput: function (e) {
    this.setData({
      'newTodo.title': e.detail
    });
  },

  bindDescriptionInput: function (e) {
    this.setData({
      'newTodo.description': e.detail
    });
  },

  bindDateChange: function (e) {
    this.setData({
      'newTodo.due_date': e.detail.value
    });
  },

  sortTodos: function (todos) {
    return todos.sort((a, b) => a.completed - b.completed);
  }
});
