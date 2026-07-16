# Token Connection Rules

## Typography

- Font: Pretendard Variable
- Figma Text Style와 CSS token을 연결
- 임의 px 사용보다 token 우선

## Color

권장 semantic token:

```text
colorBrandPrimary
colorBrandPrimaryPressed
colorSurfaceDefault
colorSurfaceSubtle
colorTextPrimary
colorTextSecondary
colorBorderDefault
colorSuccess
colorWarning
colorDanger
colorDisabled
```

## Spacing

8px base grid.

```text
space1 = 8
space2 = 16
space3 = 24
space4 = 32
space5 = 40
space6 = 48
space8 = 64
```

## Radius

```text
radiusSm
radiusMd
radiusLg
radiusXl
radiusPill
```

## Elevation

관리자 카드와 Modal에만 제한적으로 사용.

## Motion

- 빠른 상태 전환: 120~160ms
- Modal/Drawer: 180~240ms
- 과도한 spring 금지
