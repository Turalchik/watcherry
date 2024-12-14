<template>
  <div id="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Стили для базовой структуры */
#app {
  font-family: Arial, sans-serif;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}

header {
  background-color: #34495e;
  padding: 10px;
}

header nav ul {
  list-style: none;
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
}

header nav ul li {
  margin: 0 10px;
}

header nav ul li a {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 1.2em;
}

header nav ul li a:hover {
  text-decoration: underline;
}

main {
  padding: 20px;
  min-height: 80vh;
}
</style>
