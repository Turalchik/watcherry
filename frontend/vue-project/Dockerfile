# Dockerfile для фронтенда (frontend/vue-project/Dockerfile)

# Используем базовый образ Node.js
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем Vite
RUN npm install vite --save-dev
RUN npm install vite vite-plugin-vue-devtools --save-dev


# Открываем порт, который использует Vite
EXPOSE 5173

# Команда для запуска приложения
CMD ["npm", "run", "dev"]
