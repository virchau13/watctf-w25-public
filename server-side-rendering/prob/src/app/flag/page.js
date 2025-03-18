import styles from "../page.module.css";
import { cookies } from 'next/headers';
import sha256 from 'js-sha256';
import AdminPageImpl from './adminpageimpl';

const ADMIN_PW_HASH = "1b504583e27618fd2d5c5c07935f89e34b29cc60d34f045ed7a3567d68b89946";

export default async function AdminPanel() {

  const cookieStore = await cookies();
  let token = cookieStore.get('token');
  let isAdmin;
  if (typeof token === 'string' && sha256.hex(token) == ADMIN_PW_HASH) {
    isAdmin = true;
  } else {
    isAdmin = false;
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <AdminPageImpl isAdmin={isAdmin} />
      </main>
    </div>
  );
}
