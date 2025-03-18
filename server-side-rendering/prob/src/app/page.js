import Image from "next/image";
import styles from "./page.module.css";
import catInTheDark from '../../public/cat-in-the-dark.png';

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
          Did you know that in 2011, scientists genetically modified cats
          to glow in the dark?
          <div style={{display:'flex',}}>
            <Image
              src={catInTheDark}
              alt="Cat in the dark"
              width={325}
              height={405}
            />
            <Image
              src="/cats-now-glowing.png"
              alt="Cats now glowing"
              width={539}
              height={405}
            />
          </div>
        <p>Wongsrikeao, P., Saenz, D., Rinkoski, T. et al. Antiviral restriction factor transgenesis in the domestic cat. <i>Nat Methods</i> 8, 853–859 (2011). <a href="https://doi.org/10.1038/nmeth.1703">https://doi.org/10.1038/nmeth.1703</a></p>

      </main>
    </div>
  );
}
