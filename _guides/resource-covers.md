# 일반 자료 표지 출처

아래 이미지는 2026-10-17에 공식 PDF의 첫 페이지를 축소하여 만들었습니다.
원문 내용이나 로고는 수정하지 않았으며 각 자료의 기존 원문 링크를 유지합니다.
표지는 `images/resources/covers/`에 저장합니다.

| 이미지 | 공식 원문 PDF |
| --- | --- |
| `mars-planetary-protection-primer-2026.jpg` | [NASA/JPL Mars Planetary Protection Primer](https://sma.nasa.gov/docs/default-source/sma-disciplines-and-programs/planetary-protection/mars-planetary-protection-primer_cat-iii_2026.pdf?sfvrsn=8a3ad3f8_0) |
| `systems-engineering-handbook.jpg` | [NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf) |
| `small-spacecraft-2026.jpg` | [NASA State-of-the-Art of Small Spacecraft Technology 2026](https://www.nasa.gov/wp-content/uploads/2026/05/soa-2026.pdf) |

원본 PDF를 로컬로 받은 뒤 다음 명령으로 재생성할 수 있습니다.

```sh
pdftoppm -f 1 -l 1 -singlefile -scale-to 700 -jpeg -jpegopt quality=85 input.pdf output-cover
```

`_data/library.yaml`의 `cover` 경로로 연결하며, CMS의 **자료 관리 → 일반 자료 → 표지 이미지 (선택)**에서도 변경할 수 있습니다. 외부 문서가 새 판으로 바뀌면 링크와 설명을 확인하고 표지도 함께 교체하세요. CMS에서 직접 업로드한 PDF의 자동 표지는 별도 출처 이미지 파일을 커밋할 필요가 없습니다.
