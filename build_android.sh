#!/bin/bash
# Скрипт для сборки Android APK с помощью Buildozer

set -e  # Остановка при ошибке

echo "=== Сборка Android APK для Крестики-Нолики ==="
echo "==============================================="

# Проверка наличия Buildozer
if ! command -v buildozer &> /dev/null; then
    echo "Buildozer не установлен. Устанавливаем..."
    pip install buildozer
fi

# Проверка файла buildozer.spec
if [ ! -f buildozer.spec ]; then
    echo "Файл buildozer.spec не найден. Используйте buildozer init для его создания."
    exit 1
fi

# Определяем тип сборки
read -p "Выберите тип сборки (debug/release): " BUILD_TYPE
if [ "$BUILD_TYPE" != "debug" ] && [ "$BUILD_TYPE" != "release" ]; then
    echo "Неверный тип сборки. Допустимые значения: debug, release"
    exit 1
fi

echo "Начинаем сборку $BUILD_TYPE..."

if [ "$BUILD_TYPE" == "release" ]; then
    # Проверяем наличие keystore для release-сборки
    if [ ! -f tictactoe.keystore ]; then
        echo "Для релизной сборки требуется файл keystore."
        read -p "Создать новый keystore? (y/n): " CREATE_KEYSTORE
        
        if [ "$CREATE_KEYSTORE" == "y" ]; then
            echo "Создание нового keystore файла..."
            keytool -genkey -v -keystore tictactoe.keystore -alias tictactoe -keyalg RSA -keysize 2048 -validity 10000
            
            # Обновляем buildozer.spec для релизной сборки
            sed -i 's/android.keystore =/android.keystore = tictactoe.keystore/g' buildozer.spec
            sed -i 's/android.keyalias =/android.keyalias = tictactoe/g' buildozer.spec
        else
            echo "Без keystore невозможно создать релизную сборку."
            exit 1
        fi
    fi
fi

# Запуск сборки
echo "Запускаем buildozer android $BUILD_TYPE"
buildozer android $BUILD_TYPE

echo ""
echo "Сборка завершена!"

# Проверяем результат сборки
if [ -d ./bin ]; then
    echo "APK файлы в директории ./bin:"
    ls -la ./bin/*.apk
    echo ""
    echo "Для установки на подключенное устройство Android, выполните:"
    echo "adb install -r ./bin/[имя_файла].apk"
else
    echo "Директория ./bin не найдена. Возможно произошла ошибка при сборке."
    exit 1
fi

echo "==============================================="
echo "Подробные инструкции по установке на Android: смотрите файл ANDROID_BUILD.md"