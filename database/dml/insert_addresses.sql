INSERT INTO
    addresses (
        post_code,
        prefecture,
        city,
        street,
        position
    )
VALUES
    (
        '1600023',
        '東京都',
        '新宿区',
        '西新宿',
        GeomFromText('Point(139.69369 35.6913457)')
    ),
    (
        '1610034',
        '東京都',
        '新宿区',
        '上落合',
        GeomFromText('Point(139.6873087 35.7128622)')
    )
