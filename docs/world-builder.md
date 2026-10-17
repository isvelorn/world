# World Builder · план реализации

World Builder — **логическая подсистема генерации контента**, а не обязательный восьмой репозиторий или отдельный процесс.

## Интерфейс (будущий)

`validated definition + pinned generator version + seed → preview/geometry/animation/behavior references → diagnostics + digest`.

Генерация **не меняет** игроковые данные. Новые объекты пока невозможно создавать полностью автоматически: нужна библиотека известной геометрии, сборки существ, анимаций, поведения и привязок к abilities.

## Pipeline

1. Proposal с новым определением в отдельной ветке/PR.
2. Схема и зависимости (включая canon).
3. Совместимость `required_capabilities` с game/server builder.
4. Генерация в sandbox с budget (CPU/time/memory/output).
5. Проверка коллизий, видимости, навигации и баланса; визуальный preview при необходимости.
6. Immutable artifact с digest/SHA, версия runtime, promotion через release-gate.
7. Server применяет через версионированную операцию и сохраняет receipt.

Новые `generator_id`, skeletal rigs, AI behaviors, механики, shader paths — **обновление программного движка**, а не свободное заполнение JSON.

## Условия безопасности

Никакой пользовательский Python/GLSL/C/шелл из proposal не исполняется в production. Вмешательство человека требовать для неизвестных capabilities. Качество картинки и грамотность анимации проверяются тестовым рендером, а не декларацией ИИ «готово».
